from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
import traceback
from datetime import datetime, timezone
from email import policy
from email.parser import BytesParser
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.layers.config.local_yaml_config_store import LocalYamlConfigStore
from src.pipeline.attachment_extraction.module import AttachmentExtractionModule
from src.pipeline.case_thread_binding.module import CaseThreadBindingModule
from src.pipeline.decision_layer.module import DecisionLayerModule
from src.pipeline.draft_builder.module import DraftBuilderModule
from src.pipeline.early_classification import apply_early_classification, early_classification
from src.pipeline.identity_context_enrichment.module import IdentityContextEnrichmentModule
from src.pipeline.knowledge_retrieval.module import KnowledgeRetrievalModule
from src.pipeline.llm_understanding.module import LlmUnderstandingModule
from src.pipeline.mail_import.module import MailImportModule
from src.pipeline.operator_bot import OperatorBotHandler
from src.pipeline.operator_flow import load_dossier, read_json, resolve_uid, save_dossier, write_json
from src.pipeline.telegram_bot_api import TelegramBotApiClient
from src.pipeline.telegram_operator_delivery.module import TelegramOperatorDeliveryModule
from src.shared.common.paths import resolve_project_path
from src.shared.models.pipeline_context import PipelineContext


MAILBOX_ROOT = Path("fixtures/mock_mailbox")
INBOX_DIR = MAILBOX_ROOT / "inbox"
PROCESSING_DIR = MAILBOX_ROOT / "processing"
PROCESSED_DIR = MAILBOX_ROOT / "processed"
FAILED_DIR = MAILBOX_ROOT / "failed"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the mock .eml inbox to Telegram operator demo flow")
    parser.add_argument("--artifacts-dir", default="artifacts")
    parser.add_argument("--inbox-dir", default=str(INBOX_DIR))
    parser.add_argument("--processing-dir", default=str(PROCESSING_DIR))
    parser.add_argument("--processed-dir", default=str(PROCESSED_DIR))
    parser.add_argument("--failed-dir", default=str(FAILED_DIR))
    parser.add_argument("--poll-seconds", type=int, default=None)
    parser.add_argument("--poll-timeout", type=int, default=5)
    parser.add_argument("--strict-llm", action="store_true")
    parser.add_argument("--once", action="store_true", help="Process current inbox once and exit")
    args = parser.parse_args()

    inbox_dir = resolve_project_path(args.inbox_dir)
    processing_dir = resolve_project_path(args.processing_dir)
    processed_dir = resolve_project_path(args.processed_dir)
    failed_dir = resolve_project_path(args.failed_dir)
    ensure_mock_mailbox_dirs(
        inbox_dir=inbox_dir,
        processing_dir=processing_dir,
        processed_dir=processed_dir,
        failed_dir=failed_dir,
    )

    poll_seconds = resolve_poll_seconds(args.poll_seconds)
    if args.once:
        sent_cards, had_error = process_pending_emails(
            inbox_dir=inbox_dir,
            processing_dir=processing_dir,
            processed_dir=processed_dir,
            failed_dir=failed_dir,
            artifacts_dir=args.artifacts_dir,
            strict_llm=args.strict_llm,
            print_empty=True,
        )
        if sent_cards:
            run_telegram_polling(
                artifacts_dir=args.artifacts_dir,
                poll_seconds=poll_seconds,
                poll_timeout=args.poll_timeout,
            )
        if had_error:
            raise SystemExit(1)
        return

    run_watch_loop(
        inbox_dir=inbox_dir,
        processed_dir=processed_dir,
        processing_dir=processing_dir,
        failed_dir=failed_dir,
        artifacts_dir=args.artifacts_dir,
        strict_llm=args.strict_llm,
        poll_seconds=poll_seconds,
        poll_timeout=args.poll_timeout,
    )


def run_watch_loop(
    *,
    inbox_dir: Path,
    processing_dir: Path,
    processed_dir: Path,
    failed_dir: Path,
    artifacts_dir: str,
    strict_llm: bool,
    poll_seconds: int,
    poll_timeout: int,
) -> None:
    print(
        "[mock_flow] started "
        f"mode=watch inbox={inbox_dir} processing={processing_dir} processed={processed_dir} failed={failed_dir} "
        f"telegram_poll_seconds={poll_seconds} poll_timeout={poll_timeout}"
    )

    try:
        while True:
            # First catch /start and operator comments, then process mailbox.
            # Otherwise a fresh email can be processed before the operator DM is registered.
            if poll_seconds > 0:
                try:
                    run_telegram_polling(artifacts_dir=artifacts_dir, poll_seconds=1, poll_timeout=1)
                except Exception as exc:
                    print(f"[mock_flow] telegram_polling=error error={exc}")

            process_pending_emails(
                inbox_dir=inbox_dir,
                processing_dir=processing_dir,
                processed_dir=processed_dir,
                failed_dir=failed_dir,
                artifacts_dir=artifacts_dir,
                strict_llm=strict_llm,
                print_empty=False,
            )

            telegram_cycle_seconds = resolve_telegram_cycle_seconds(
                poll_seconds=poll_seconds,
                poll_timeout=poll_timeout,
            )
            if telegram_cycle_seconds > 0:
                try:
                    run_telegram_polling(
                        artifacts_dir=artifacts_dir,
                        poll_seconds=telegram_cycle_seconds,
                        poll_timeout=poll_timeout,
                    )
                except Exception as exc:
                    print(f"[mock_flow] telegram_polling=error error={exc}")
                    time.sleep(1)
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        print("[mock_flow] stopped by operator")


def process_pending_emails(
    *,
    inbox_dir: Path,
    processing_dir: Path,
    processed_dir: Path,
    failed_dir: Path,
    artifacts_dir: str,
    strict_llm: bool,
    print_empty: bool,
    telegram_delivery_mode: str = "real",
) -> tuple[int, bool]:
    eml_files = discover_eml_files(inbox_dir)
    if not eml_files:
        if print_empty:
            print(f"[mock_flow] no .eml files found in {inbox_dir}")
        return 0, False

    sent_cards = 0
    had_error = False
    for eml_path in eml_files:
        claimed_path = claim_eml_file(eml_path, processing_dir)
        if claimed_path is None:
            print(f"[mock_flow] uid={eml_path.stem} claim=skipped reason=file_disappeared")
            continue
        result = process_eml(
            eml_path=claimed_path,
            processed_dir=processed_dir,
            failed_dir=failed_dir,
            artifacts_dir=artifacts_dir,
            strict_llm=strict_llm,
            telegram_delivery_mode=telegram_delivery_mode,
        )
        sent_cards += 1 if result.get("telegram") == "sent" else 0
        had_error = had_error or bool(result.get("failed"))
        print(format_console_line(result))

    return sent_cards, had_error


def resolve_telegram_cycle_seconds(*, poll_seconds: int, poll_timeout: int) -> int:
    if poll_seconds <= 0:
        return 0
    return min(max(int(poll_seconds), 1), max(int(poll_timeout), 1))


def ensure_mock_mailbox_dirs(*, inbox_dir: Path, processing_dir: Path, processed_dir: Path, failed_dir: Path) -> None:
    inbox_dir.mkdir(parents=True, exist_ok=True)
    processing_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    failed_dir.mkdir(parents=True, exist_ok=True)


def discover_eml_files(inbox_dir: Path) -> list[Path]:
    return sorted(path for path in inbox_dir.glob("*.eml") if path.is_file())


def claim_eml_file(source: Path, processing_dir: Path) -> Path | None:
    if not source.exists():
        return None
    processing_dir.mkdir(parents=True, exist_ok=True)
    target = processing_dir / source.name
    if target.exists():
        target = processing_dir / f"{source.stem}_{timestamp()}{source.suffix}"
    try:
        return Path(shutil.move(str(source), str(target)))
    except FileNotFoundError:
        return None


def process_eml(
    *,
    eml_path: Path,
    processed_dir: Path,
    failed_dir: Path,
    artifacts_dir: str,
    strict_llm: bool,
    telegram_delivery_mode: str = "real",
    force_fallback_llm: bool = False,
) -> dict[str, Any]:
    preview = read_eml_preview(eml_path)
    run_id = f"mock-flow-{safe_stem(eml_path.stem)}-{timestamp()}"
    result: dict[str, Any] = {
        "uid": eml_path.stem,
        "from": preview["from"],
        "subject": preview["subject"],
        "import": "pending",
        "attach": "pending",
        "class": "pending",
        "enrich": "pending",
        "bind": "pending",
        "understanding": "pending",
        "retrieval": "pending",
        "decision": "pending",
        "draft": "pending",
        "telegram": "pending",
        "failed": False,
    }
    context = PipelineContext(run_id=run_id)

    try:
        import_result = MailImportModule(
            config={
                "enabled": True,
                "mode": "fixture",
                "fixture_path": str(eml_path),
                "fixture_ref": eml_path.stem,
                "mailbox": "mock_mailbox",
                "email_address": "info@mooon.by",
            },
            artifacts_dir=artifacts_dir,
        ).run(context)
        require_ok("mail_import", import_result)
        result["import"] = "ok"

        dossier_path = find_ref(import_result.artifact_refs, ".md")
        raw_path = find_ref(import_result.artifact_refs, ".eml")
        if not dossier_path:
            raise RuntimeError("mail_import did not produce parsed dossier")

        attachment_result = AttachmentExtractionModule(
            parsed_email_path=dossier_path,
            raw_email_path=raw_path or str(eml_path),
        ).run(context)
        require_ok("attachment_extraction", attachment_result)
        result["attach"] = str(attachment_result.metrics.get("items_count", 0))

        payload = load_dossier(dossier_path)
        classification = apply_early_classification(payload)
        save_dossier(dossier_path, payload)
        result["class"] = classification.get("classification") or "unknown"

        enrichment_result = IdentityContextEnrichmentModule(
            parsed_email_path=dossier_path,
            attachment_report_path=str(attachment_result.metrics.get("report_path") or ""),
        ).run(context)
        require_ok("identity_context_enrichment", enrichment_result)
        result["enrich"] = enrichment_result.status

        binding_result = CaseThreadBindingModule(parsed_email_path=dossier_path, artifacts_dir=artifacts_dir).run(context)
        require_ok("case_thread_binding", binding_result)
        result["bind"] = str(binding_result.metrics.get("binding_rule") or binding_result.status)

        if force_fallback_llm:
            write_fallback_understanding(dossier_path, ["forced fallback for flow acceptance smoke"])
            result["understanding"] = "fallback"
        else:
            llm_result = LlmUnderstandingModule(
                dossier_path=dossier_path,
                config_path="config/structured_understanding.xlsx",
            ).run(context)
            if llm_result.status == "ok":
                result["understanding"] = "ok"
            elif strict_llm:
                require_ok("llm_understanding", llm_result)
            else:
                write_fallback_understanding(dossier_path, llm_result.notes)
                result["understanding"] = "fallback"

        retrieval_result = KnowledgeRetrievalModule(dossier_path=dossier_path).run(context)
        require_ok("knowledge_retrieval", retrieval_result)
        result["retrieval"] = str(retrieval_result.metrics.get("status") or retrieval_result.status)

        decision_result = DecisionLayerModule(dossier_path=dossier_path).run(context)
        require_ok("decision_layer", decision_result)
        result["decision"] = str(decision_result.metrics.get("response_mode_final") or decision_result.status)

        draft_result = DraftBuilderModule(dossier_path=dossier_path).run(context)
        require_ok("draft_builder", draft_result)
        draft_status = str(draft_result.metrics.get("status") or "ok")
        if draft_status == "skipped":
            result["draft"] = "skipped"
        else:
            result["draft"] = f"v{draft_result.metrics.get('latest_revision')}"

        telegram_result = TelegramOperatorDeliveryModule(
            dossier_path=dossier_path,
            artifacts_dir=artifacts_dir,
            delivery_mode=telegram_delivery_mode,
        ).run(context)
        require_ok("telegram_operator_delivery", telegram_result)
        delivery_mode = str(telegram_result.metrics.get("telegram_delivery_mode") or "")
        result["telegram"] = "sent" if telegram_result.metrics.get("telegram_message_id") else delivery_mode or "artifact_only"
        result["telegram_chat_id"] = telegram_result.metrics.get("telegram_chat_id")
        result["telegram_message_id"] = telegram_result.metrics.get("telegram_message_id")
        result["telegram_delivery_mode"] = delivery_mode
        result["card_artifact_path"] = telegram_result.metrics.get("card_artifact_path")
        result["dossier_path"] = dossier_path

        payload = load_dossier(dossier_path)
        result["uid"] = resolve_uid(payload)
        result["case_id"] = ((payload.get("modules") or {}).get("case_thread_binding") or {}).get("case_id")
        result["thread_id"] = ((payload.get("modules") or {}).get("case_thread_binding") or {}).get("thread_id")

        move_unique(eml_path, processed_dir)
    except Exception as exc:
        result["failed"] = True
        result["error"] = str(exc)
        result["error_artifact_path"] = write_error_artifact(
            artifacts_dir=artifacts_dir,
            eml_path=eml_path,
            run_id=run_id,
            preview=preview,
            result=result,
            error=exc,
        )
        move_unique(eml_path, failed_dir)

    return result


def run_telegram_polling(*, artifacts_dir: str, poll_seconds: int, poll_timeout: int) -> dict[str, Any]:
    if poll_seconds <= 0:
        return {"status": "skipped", "processed_updates": 0}

    client = TelegramBotApiClient.from_config()
    if client is None:
        raise RuntimeError("Telegram bot token is not configured")

    handler = OperatorBotHandler(artifacts_dir=artifacts_dir, client=client)
    state_path = resolve_project_path(artifacts_dir) / "state" / "operator_bot_updates.json"
    deadline = time.monotonic() + poll_seconds
    processed_updates = 0

    while time.monotonic() < deadline:
        state = read_json(state_path, {"offset": None})
        offset = state.get("offset") if isinstance(state, dict) else None
        remaining = max(deadline - time.monotonic(), 0)
        timeout_value = min(max(int(remaining), 1), max(int(poll_timeout), 1))
        updates = client.get_updates(offset=offset, timeout=timeout_value)
        if not updates.get("ok"):
            raise RuntimeError(f"Telegram getUpdates failed: {updates.get('error')}")

        for update in updates.get("result") or []:
            processed_updates += 1
            update_id = int(update.get("update_id"))
            state = {"offset": update_id + 1}
            try:
                callback_query = update.get("callback_query")
                if callback_query:
                    message = callback_query.get("message") or {}
                    chat = message.get("chat") or {}
                    from_user = callback_query.get("from") or {}
                    callback_result = handler.handle_callback(
                        callback_data=str(callback_query.get("data") or ""),
                        chat_id=chat.get("id"),
                        message_id=int(message.get("message_id")),
                        operator_telegram_id=str(from_user.get("id") or ""),
                        operator_username=str(from_user.get("username") or ""),
                        callback_query_id=str(callback_query.get("id") or ""),
                    )
                    if callback_result.get("action"):
                        print(
                            "[mock_flow] telegram_callback="
                            f"{callback_result.get('status')} action={callback_result.get('action')} "
                            f"chat_id={chat.get('id')} user_id={callback_result.get('operator_telegram_id') or from_user.get('id') or ''}"
                        )

                message = update.get("message")
                if message and message.get("text"):
                    chat = message.get("chat") or {}
                    from_user = message.get("from") or {}
                    reply_to = message.get("reply_to_message") or {}
                    reply_to_message_id = reply_to.get("message_id") if isinstance(reply_to, dict) else None
                    message_result = handler.handle_operator_message(
                        chat_id=chat.get("id"),
                        text=str(message.get("text") or ""),
                        message_id=int(message.get("message_id")),
                        reply_to_message_id=int(reply_to_message_id) if reply_to_message_id else None,
                        operator_telegram_id=str(from_user.get("id") or ""),
                        operator_username=str(from_user.get("username") or ""),
                        chat_type=str(chat.get("type") or ""),
                    )
                    if message_result.get("action"):
                        print(
                            "[mock_flow] telegram_message="
                            f"{message_result.get('status')} action={message_result.get('action')} "
                            f"reason={message_result.get('reason') or ''} "
                            f"chat_id={chat.get('id')} user_id={message_result.get('operator_telegram_id') or from_user.get('id') or ''} "
                            f"username={from_user.get('username') or ''} uid={message_result.get('uid') or ''}"
                        )
            except Exception as exc:
                print(f"[mock_flow] telegram_update=error update_id={update_id} error={exc}")
            finally:
                write_json(state_path, state)

    return {"status": "ok", "processed_updates": processed_updates}


def resolve_poll_seconds(cli_value: int | None) -> int:
    if cli_value is not None:
        return max(cli_value, 0)
    try:
        config = LocalYamlConfigStore().get_section("mock_flow")
        return max(int(config.get("telegram_poll_seconds", 300) or 300), 0)
    except Exception:
        return 300


def write_fallback_understanding(dossier_path: str, notes: list[str]) -> None:
    payload = load_dossier(dossier_path)
    headers = payload.get("headers") or {}
    body = str(payload.get("body_text") or "")
    subject = str(headers.get("subject") or "")
    sender = str(headers.get("sender") or "")
    classification = early_classification(payload)
    text = f"{subject}\n{body}".casefold()
    ticket_related = any(token in text for token in ["ticket", "билет", "оплат", "заказ", "квитанц"])
    mode = str(classification.get("response_mode_hint") or "").strip()
    if not mode:
        mode = "ask_clarifying_question" if ticket_related else "handoff_to_operator"
    summary = str(classification.get("operator_summary") or "").strip()
    if not summary:
        summary = f"Входящее письмо от {sender or 'отправителя'}: {subject or 'без темы'}."
    topic = _fallback_topic(classification, ticket_related)
    need = _fallback_need(classification, ticket_related)
    modules = payload.setdefault("modules", {})
    modules["llm_understanding"] = {
        "uid": resolve_uid(payload),
        "status": "ok",
        "backend": "deterministic_fallback",
        "model": "local-rule-fallback",
        "prompt_version": "fallback",
        "context_version": "fallback",
        "duration_ms": 0,
        "error": "; ".join(notes),
        "structured_output": {
            "summary": summary,
            "topic": topic,
            "customer_need": need,
            "entities": [{"type": "sender", "value": sender}] if sender else [],
            "confidence": 0.62,
            "response_mode": mode,
            "understanding_note": "Создано локальным fallback для demo-flow, потому что внешний LLM не вернул валидный результат.",
            "response_mode_reason": str(classification.get("classification_reason") or "Flow выбрал безопасный режим обработки."),
            "suggested_next_step": str(classification.get("proposed_action_text") or "Проверить карточку и выбрать действие кнопками."),
            "risk_level": "medium",
            "needs_human": mode == "handoff_to_operator",
        },
    }
    save_dossier(dossier_path, payload)


def _fallback_topic(classification: dict[str, Any], ticket_related: bool) -> str:
    mapping = {
        "customer_support": "Клиентский вопрос по билету/оплате",
        "schedule_or_repertoire_question": "Вопрос по расписанию или репертуару",
        "business_proposal": "Бизнес-предложение",
        "candidate_or_portfolio": "Кандидат или портфолио",
        "training_invitation": "Приглашение на обучение",
        "gratitude_or_case_closed": "Благодарность / вопрос закрыт",
        "service_notification": "Служебное уведомление",
        "action_required_notification": "Служебное уведомление, требующее действия",
        "newsletter_or_promo": "Рекламная рассылка",
        "security_or_no_reply_noise": "No-reply/security уведомление",
        "bounce_or_delivery_noise": "Техническое уведомление о доставке",
    }
    value = str(classification.get("classification") or "")
    return mapping.get(value) or ("Вопрос по билету или оплате" if ticket_related else "Входящее письмо")


def _fallback_need(classification: dict[str, Any], ticket_related: bool) -> str:
    value = str(classification.get("classification") or "")
    if value == "newsletter_or_promo":
        return "Ответ клиенту не требуется; письмо можно игнорировать."
    if value == "gratitude_or_case_closed":
        return "Ответ клиенту не требуется; вопрос уже закрыт, отправитель благодарит."
    if value == "security_or_no_reply_noise":
        return "Проверить как служебное security-уведомление; клиентский ответ не нужен."
    if value == "action_required_notification":
        return "Зафиксировать служебное уведомление и уведомить ответственных stub-действием."
    if value == "candidate_or_portfolio":
        return "Передать предложение/портфолио ответственным на ручную обработку."
    if value == "training_invitation":
        return "Передать приглашение на обучение ответственным на ручную обработку."
    if value == "schedule_or_repertoire_question":
        return "Понять, возможен ли показ; без live schedule connector передать ответственным."
    if ticket_related:
        return "Получить помощь по билету или оплате."
    return "Определить ответственного и обработать вручную."


def require_ok(module_name: str, result: Any) -> None:
    if result.status != "ok":
        raise RuntimeError(f"{module_name} status={result.status}: {'; '.join(result.notes)}")


def find_ref(refs: list[str], suffix: str) -> str:
    for ref in refs:
        if str(ref).lower().endswith(suffix):
            return str(ref)
    return ""


def read_eml_preview(path: Path) -> dict[str, str]:
    try:
        message = BytesParser(policy=policy.default).parsebytes(path.read_bytes())
        return {
            "from": str(message.get("from") or "").strip(),
            "subject": str(message.get("subject") or "").strip(),
        }
    except Exception:
        return {"from": "", "subject": ""}


def write_error_artifact(
    *,
    artifacts_dir: str,
    eml_path: Path,
    run_id: str,
    preview: dict[str, str],
    result: dict[str, Any],
    error: Exception,
) -> str:
    payload = {
        "status": "error",
        "run_id": run_id,
        "source_eml_path": str(eml_path),
        "preview": preview,
        "result": result,
        "error": str(error),
        "traceback": traceback.format_exc(),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    target = resolve_project_path(artifacts_dir) / "mock_mailbox_errors" / f"{safe_stem(eml_path.stem)}_{timestamp()}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(target)


def move_unique(source: Path, target_dir: Path) -> Path:
    if not source.exists():
        return source
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / source.name
    if target.exists():
        target = target_dir / f"{source.stem}_{timestamp()}{source.suffix}"
    shutil.move(str(source), str(target))
    return target


def format_console_line(result: dict[str, Any]) -> str:
    parts = [
        f"uid={result.get('uid') or ''}",
        f"from={result.get('from') or ''}",
        f"subject=\"{str(result.get('subject') or '').replace(chr(34), chr(39))}\"",
        f"import={result.get('import')}",
        f"attach={result.get('attach')}",
        f"class={result.get('class')}",
        f"enrich={result.get('enrich')}",
        f"bind={result.get('bind')}",
        f"understanding={result.get('understanding')}",
        f"retrieval={result.get('retrieval')}",
        f"decision={result.get('decision')}",
        f"draft={result.get('draft')}",
        f"telegram={result.get('telegram')}",
    ]
    if result.get("failed"):
        parts.append(f"error_artifact={result.get('error_artifact_path')}")
    return "[mock_flow] " + " ".join(parts)


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")


def safe_stem(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in value) or "message"


if __name__ == "__main__":
    main()
