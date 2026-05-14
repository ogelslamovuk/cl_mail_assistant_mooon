from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.pipeline.draft_builder.module import DraftBuilderModule
from src.pipeline.operator_bot import OperatorBotHandler
from src.pipeline.operator_flow import load_dossier, read_json
from src.pipeline.telegram_operator_delivery.module import TelegramOperatorDeliveryModule
from src.runners.run_mock_mailbox_flow import process_eml, timestamp
from src.shared.common.message_dossier import write_message_dossier
from src.shared.common.paths import resolve_project_path
from src.shared.models.pipeline_context import PipelineContext


CURATED_UIDS = ["26815", "26816", "26817", "26818", "26819", "26820", "26823"]

EXPECTED_CLASSES = {
    "26815": {"candidate_or_portfolio"},
    "26816": {"newsletter_or_promo"},
    "26817": {"gratitude_or_case_closed"},
    "26818": {"business_proposal"},
    "26819": {"training_invitation"},
    "26820": {"candidate_or_portfolio"},
    "26823": {"customer_support"},
}

ENRICHMENT_SKIPPED = set(CURATED_UIDS) - {"26823"}
KNOWLEDGE_SKIPPED = set(CURATED_UIDS) - {"26823"}
DRAFT_SKIPPED = set(CURATED_UIDS) - {"26823"}
ACTION_BUTTON_UIDS = {"26815", "26818", "26819", "26820"}

FORBIDDEN_CARD_TEXT = [
    "Смысл письма: Здравствуйте",
    "Смысл письма: Добрый день",
    "Суть обращения: Здравствуйте",
    "Суть обращения: Добрый день",
    "fallback meaningful message",
    "notify_department_stub",
    "mark_manual_processing",
    "stub-действие",
    "PK\x03\x04",
    "[Content_Types].xml",
    "rescue_candidates",
    "confidence:",
    " / Enrichment",
    "в enrichment",
]


def main() -> None:
    root = resolve_project_path("artifacts/flow_acceptance")
    run_id = timestamp()
    artifacts_dir = root / f"run_{run_id}"
    inbox_dir = root / f"tmp_inbox_{run_id}"
    processed_dir = root / f"tmp_processed_{run_id}"
    failed_dir = root / f"tmp_failed_{run_id}"
    for path in [artifacts_dir, inbox_dir, processed_dir, failed_dir]:
        path.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    for uid in CURATED_UIDS:
        source = _find_source(uid)
        if source is None:
            rows.append(_missing_row(uid))
            continue
        target = inbox_dir / f"raw_email_{uid}.eml"
        shutil.copy2(source, target)
        result = process_eml(
            eml_path=target,
            processed_dir=processed_dir,
            failed_dir=failed_dir,
            artifacts_dir=str(artifacts_dir),
            strict_llm=False,
            telegram_delivery_mode="artifact_only",
            force_fallback_llm=True,
        )
        rows.append(_row_from_result(uid, source, result))

    callback_report = _run_fake_callback_tests(artifacts_dir, rows)
    has_missing = any(row["source_status"] == "missing_fixture" for row in rows)
    all_available_passed = all(row["passed"] or row["source_status"] == "missing_fixture" for row in rows)
    callbacks_passed = callback_report["status"] == "passed"
    status = "ok" if all_available_passed and callbacks_passed and not has_missing else "failed"
    if has_missing and all_available_passed and callbacks_passed:
        status = "partial"

    report = {
        "status": status,
        "created_at": run_id,
        "rows": rows,
        "fake_telegram_callbacks": callback_report,
    }
    root.mkdir(parents=True, exist_ok=True)
    json_path = root / "flow_acceptance_latest.json"
    md_path = root / "flow_acceptance_latest.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(_render_markdown(report), encoding="utf-8")
    print(f"[flow_acceptance] report_json={json_path}")
    print(f"[flow_acceptance] report_md={md_path}")
    print(f"[flow_acceptance] status={report['status']}")
    if report["status"] not in {"ok", "partial"}:
        raise SystemExit(1)


def _find_source(uid: str) -> Path | None:
    roots = [
        resolve_project_path("fixtures/mock_mailbox/inbox"),
        resolve_project_path("fixtures/mock_mailbox/processed"),
        resolve_project_path("fixtures/mock_mailbox/failed"),
        resolve_project_path("fixtures/mock_mailbox/processing"),
    ]
    for root in roots:
        if not root.exists():
            continue
        exact = root / f"raw_email_{uid}.eml"
        if exact.exists():
            return exact
        matches = sorted(root.glob(f"*{uid}*.eml"))
        if matches:
            return matches[0]
    return None


def _missing_row(uid: str) -> dict[str, Any]:
    return {
        "uid": uid,
        "source_status": "missing_fixture",
        "classification": "",
        "operator_summary": "",
        "enrichment_status": "",
        "knowledge_status": "",
        "draft_status": "",
        "telegram_card_artifact": "",
        "operator_buttons_present": [],
        "attachments_present": False,
        "expected_result": sorted(EXPECTED_CLASSES.get(uid, [])),
        "passed": False,
        "notes": ["missing fixture"],
    }


def _row_from_result(uid: str, source: Path, result: dict[str, Any]) -> dict[str, Any]:
    notes: list[str] = []
    if result.get("failed"):
        notes.append(str(result.get("error") or "flow failed"))
        return _failed_row(uid, source, notes)

    dossier_path = str(result.get("dossier_path") or "")
    payload = load_dossier(dossier_path)
    modules = payload.get("modules") or {}
    early = modules.get("early_classification") or {}
    enrichment = (modules.get("identity_context_enrichment") or {}).get("result") or {}
    knowledge = modules.get("knowledge_retrieval") or {}
    draft = modules.get("draft_builder") or {}
    delivery = modules.get("telegram_operator_delivery") or {}
    card_path = str(delivery.get("card_artifact_path") or result.get("card_artifact_path") or "")
    card = read_json(card_path, {}) if card_path else {}
    keyboard = card.get("keyboard") if isinstance(card, dict) else []
    buttons = [str(item.get("label") or "") for item in keyboard or [] if isinstance(item, dict)]
    card_text = str(card.get("card_text") or "") if isinstance(card, dict) else ""
    attachments = ((modules.get("attachment_extraction") or {}).get("items") or [])

    classification = str(early.get("classification") or "")
    expected = EXPECTED_CLASSES.get(uid, set())
    if expected and classification not in expected:
        notes.append(f"classification expected {sorted(expected)}, got {classification}")
    if uid in ENRICHMENT_SKIPPED and enrichment.get("ticket_db_status") != "skipped":
        notes.append(f"enrichment expected skipped, got {enrichment.get('ticket_db_status')}")
    if uid in KNOWLEDGE_SKIPPED and knowledge.get("status") != "skipped":
        notes.append(f"knowledge expected skipped, got {knowledge.get('status')}")
    if uid in DRAFT_SKIPPED and draft.get("status") != "skipped":
        notes.append(f"draft expected skipped, got {draft.get('status')}")
    if uid in ACTION_BUTTON_UIDS and "⚡ Выполнить действие" not in buttons:
        notes.append("action button missing")
    if uid not in ACTION_BUTTON_UIDS and "⚡ Выполнить действие" in buttons:
        notes.append("unexpected action button")
    if uid == "26819" and not attachments:
        notes.append("attachments expected but missing")
    if uid == "26819":
        _expect_text(card_text, "DOCX", notes)
        _expect_text(card_text, "PDF", notes)
        _expect_text(card_text, "регистрационная форма", notes)
        _expect_text(card_text, "архив", notes)
    if uid == "26817":
        _expect_text(card_text, "пригласительным решён", notes)
        _expect_text(card_text, "не отвечать", notes)
    if uid == "26818":
        _expect_text(card_text, "короткометраж", notes)
        _expect_text(card_text, "партнёрств", notes)
        if "вопрос по репертуару" in card_text:
            notes.append("26818 incorrectly shown as repertoire question")
    if uid == "26820":
        _expect_text(card_text, "Мария", notes)
        _expect_text(card_text, "практи", notes)
    if uid == "26823":
        _expect_text(card_text, "Билет найден", notes)
        _expect_text(card_text, "заказ 7056395", notes)
        _expect_text(card_text, "Дьявол носит Prada", notes)
        _expect_text(card_text, "электронный билет", notes)
        _expect_text(card_text, "История переписки</b>\nотсутствует", notes)
        _expect_text(card_text, "отправить гостю инструкцию по возврату", notes)
        forbidden_ticket_text = [
            "Email или телефон, указанный при покупке",
            "Номер заказа или билета",
            "уточнить номер заказа",
            "Билет #",
            "внутренний DB id",
        ]
        bad_ticket = [bad for bad in forbidden_ticket_text if bad.casefold() in card_text.casefold()]
        if bad_ticket:
            notes.append(f"ticket/enrichment forbidden text found: {bad_ticket}")

    bad = [bad for bad in FORBIDDEN_CARD_TEXT if bad in card_text]
    if bad:
        notes.append(f"forbidden operator-facing text found: {bad}")
    if card_text.count("<b>Что предлагает система</b>") > 1:
        notes.append("duplicated system proposal heading")
    if "Суть обращения:" not in card_text:
        notes.append("operator summary block missing")

    return {
        "uid": uid,
        "source_status": "found",
        "source_path": str(source),
        "dossier_path": dossier_path,
        "classification": classification,
        "operator_summary": str(early.get("operator_summary") or ""),
        "enrichment_status": str(enrichment.get("ticket_db_status") or ""),
        "knowledge_status": str(knowledge.get("status") or ""),
        "draft_status": str(draft.get("status") or "ok"),
        "telegram_card_artifact": card_path,
        "operator_buttons_present": buttons,
        "attachments_present": bool(attachments),
        "expected_result": sorted(expected),
        "passed": not notes,
        "notes": notes or ["ok"],
    }


def _failed_row(uid: str, source: Path, notes: list[str]) -> dict[str, Any]:
    return {
        "uid": uid,
        "source_status": "found",
        "source_path": str(source),
        "classification": "",
        "operator_summary": "",
        "enrichment_status": "",
        "knowledge_status": "",
        "draft_status": "",
        "telegram_card_artifact": "",
        "operator_buttons_present": [],
        "attachments_present": False,
        "expected_result": sorted(EXPECTED_CLASSES.get(uid, [])),
        "passed": False,
        "notes": notes,
    }


def _expect_text(text: str, expected: str, notes: list[str]) -> None:
    if expected.casefold() not in text.casefold():
        notes.append(f"expected card text missing: {expected}")


def _run_fake_callback_tests(artifacts_dir: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    client = FakeTelegramClient()
    handler = OperatorBotHandler(artifacts_dir=str(artifacts_dir), client=client)
    checks: list[dict[str, Any]] = []

    try:
        approve_fixture = _create_draft_callback_fixture(artifacts_dir)
        approve_card = read_json(approve_fixture["card_path"], {})
        _click(handler, approve_card, "needs_edit", client, callback_id="cb_draft_needs_edit")
        pending = read_json(artifacts_dir / "state" / "operator_bot_pending.json", {})
        _record(checks, "revision_waiting_state", str(approve_card["telegram_chat_id"]) in (pending.get("pending") or {}))
        revision_result = handler.handle_operator_message(
            chat_id=approve_card["telegram_chat_id"],
            text="Добавь просьбу указать номер заказа.",
            operator_telegram_id="101",
            operator_username="demo_operator",
        )
        _record(checks, "revision_artifact_created", bool(revision_result.get("revision_request_path")))
        revised_payload = load_dossier(approve_fixture["dossier_path"])
        latest_revision = ((revised_payload.get("modules") or {}).get("draft_builder") or {}).get("latest_revision")
        _record(checks, "draft_revision_created", latest_revision == 2)
        revised_card = read_json(str(revision_result.get("card_artifact_path") or ""), {})
        _record(checks, "revision_card_sent", "<b>Черновик v2</b>" in str(revised_card.get("card_text") or ""))
        _record(checks, "revision_comment_in_card", "Комментарий оператора" in str(revised_card.get("card_text") or "") and "Добавь просьбу указать номер заказа." in str(revised_card.get("card_text") or ""))
        _record(checks, "revision_card_edited", any(item.get("operation") == "editMessageText" and item.get("ok") for item in revision_result.get("bot_api_operations") or []))
        approve_result = _click(handler, revised_card, "approve", client, callback_id="cb_draft_approve")
        mock_refs = approve_result.get("mock_reply_refs") or []
        reply_json = read_json(mock_refs[1], {}) if len(mock_refs) > 1 else {}
        _record(checks, "approve_uses_latest_revision", reply_json.get("draft_revision") == 2)
    except Exception as exc:
        _record(checks, "draft_revision_approve_flow", False, str(exc))

    try:
        ignore_card = _card_for_uid(rows, "26816")
        ignore_result = _click(handler, ignore_card, "ignore", client, callback_id="cb_ignore")
        ignore_card_after = read_json(str(ignore_result.get("card_artifact_path") or ""), {})
        _record(checks, "ignore_callback", "Ответ не требуется" in str(ignore_card_after.get("card_text") or ""))
    except Exception as exc:
        _record(checks, "ignore_callback", False, str(exc))

    try:
        handoff_card = _card_for_uid(rows, "26819")
        handoff_result = _click(handler, handoff_card, "handoff", client, callback_id="cb_handoff")
        handoff_card_after = read_json(str(handoff_result.get("card_artifact_path") or ""), {})
        _record(checks, "handoff_callback", "Кейс помечен для ручной обработки" in str(handoff_card_after.get("card_text") or ""))
    except Exception as exc:
        _record(checks, "handoff_callback", False, str(exc))

    try:
        action_card = _card_for_uid(rows, "26815")
        action_result = _click(handler, action_card, "action_request", client, callback_id="cb_action")
        action_payload = read_json(str(action_result.get("operator_action_path") or ""), {})
        action_card_after = read_json(str(action_result.get("card_artifact_path") or ""), {})
        action_text = str(action_payload.get("proposed_action_text") or "") + "\n" + str(action_card_after.get("card_text") or "")
        _record(checks, "action_callback_artifact", action_payload.get("status") == "stub_recorded" and action_payload.get("real_routing") is False)
        _record(checks, "action_callback_human_text", "notify_department_stub" not in action_text and "mock-режиме" in action_text)
    except Exception as exc:
        _record(checks, "action_callback", False, str(exc))

    try:
        action_revision_card = _card_for_uid(rows, "26818")
        _click(handler, action_revision_card, "needs_edit", client, callback_id="cb_action_needs_edit")
        action_revision_result = handler.handle_operator_message(
            chat_id=action_revision_card["telegram_chat_id"],
            text="Уточни, что это съёмка фильма, а не вопрос расписания.",
            operator_telegram_id="101",
            operator_username="demo_operator",
        )
        action_payload = load_dossier(str(action_revision_result.get("dossier_path") or ""))
        action_revision = ((action_payload.get("modules") or {}).get("action_suggestion_builder") or {}).get("latest_revision")
        action_revised_card = read_json(str(action_revision_result.get("card_artifact_path") or ""), {})
        _record(checks, "action_revision_created", action_revision == 2)
        _record(checks, "action_revision_card_sent", "Обновлённое действие v2" in str(action_revised_card.get("card_text") or ""))
        _record(checks, "action_revision_comment_in_card", "Комментарий оператора" in str(action_revised_card.get("card_text") or ""))
        action_after_revision = _click(handler, action_revised_card, "action_request", client, callback_id="cb_action_after_revision")
        action_artifact = read_json(str(action_after_revision.get("operator_action_path") or ""), {})
        _record(
            checks,
            "action_uses_latest_revision",
            "съёмка фильма" in str(action_artifact.get("proposed_action_text") or ""),
        )
    except Exception as exc:
        _record(checks, "action_revision_flow", False, str(exc))

    try:
        ticket_card = _card_for_uid(rows, "26823")
        delivery_result = TelegramOperatorDeliveryModule(
            dossier_path=str(ticket_card.get("source_dossier_path") or ticket_card.get("dossier_path") or ""),
            artifacts_dir=str(artifacts_dir),
            delivery_mode="real",
            client=client,
            operator_chat_id=ticket_card["telegram_chat_id"],
        ).run(PipelineContext(run_id="attachment-caption-check"))
        attachment_ops = [
            item
            for item in delivery_result.metrics.get("telegram_operations", [])
            if item.get("operation") in {"sendPhoto", "sendDocument"}
        ]
        captions = "\n".join(str(item.get("caption") or "") for item in attachment_ops)
        _record(checks, "attachment_caption_uid", "Вложение к raw_email_26823:" in captions)
        _record(checks, "attachment_caption_human", "электронный билет" in captions or "билетный документ" in captions)
    except Exception as exc:
        _record(checks, "attachment_caption", False, str(exc))

    failed = [check for check in checks if not check["passed"]]
    return {
        "status": "failed" if failed else "passed",
        "checks": checks,
        "operations_count": len(client.operations),
    }


def _create_draft_callback_fixture(artifacts_dir: Path) -> dict[str, str]:
    fixture_dir = artifacts_dir / "callback_fixtures"
    fixture_dir.mkdir(parents=True, exist_ok=True)
    dossier_path = fixture_dir / "message_callback_approve.md"
    payload = {
        "message_id": "<callback-approve@example.test>",
        "direction": "inbound",
        "headers": {
            "sender": "guest@example.test",
            "subject": "Не пришёл билет",
            "sent_at": "2026-05-13T10:00:00+03:00",
            "to": ["info@mooon.by"],
            "cc": [],
        },
        "body_text": "Оплатил билет онлайн, но письмо с билетом не пришло.",
        "metadata": {"uid": "callback_approve"},
        "modules": {
            "case_thread_binding": {
                "case_id": "case-callback-approve",
                "thread_id": "thread-callback-approve",
                "thread_history": [],
            },
            "llm_understanding": {
                "status": "ok",
                "structured_output": {
                    "summary": "Гость оплатил билет, но не получил письмо.",
                    "topic": "Не пришёл электронный билет",
                    "customer_need": "Получить билет или инструкцию по восстановлению.",
                    "entities": [{"type": "email", "value": "guest@example.test"}],
                    "response_mode": "ask_clarifying_question",
                    "response_mode_reason": "Нужно уточнить номер заказа или контакт.",
                },
            },
            "knowledge_retrieval": {
                "status": "found",
                "matched_items": [
                    {
                        "id": "kb_system_ticket_sender",
                        "title": "Адрес отправителя электронных билетов",
                        "score": 10,
                        "template_hint": "Письмо с билетами отправляется с адреса ticket@silverscreen.by.",
                    }
                ],
            },
            "decision_layer": {
                "status": "ok",
                "response_mode_final": "ask_clarifying_question",
                "decision_reason": "Не хватает номера заказа или контактных данных для проверки.",
                "missing_data": ["Номер заказа или email/телефон, указанный при покупке."],
                "risks": [],
            },
        },
    }
    write_message_dossier(dossier_path, payload)
    context = PipelineContext(run_id="callback-approve-fixture")
    draft_result = DraftBuilderModule(dossier_path=str(dossier_path)).run(context)
    if draft_result.status != "ok":
        raise RuntimeError(f"Draft fixture failed: {draft_result.notes}")
    card_result = TelegramOperatorDeliveryModule(
        dossier_path=str(dossier_path),
        artifacts_dir=str(artifacts_dir),
        delivery_mode="artifact_only",
    ).run(PipelineContext(run_id="callback-approve-card"))
    if card_result.status != "ok":
        raise RuntimeError(f"Card fixture failed: {card_result.notes}")
    return {
        "dossier_path": str(dossier_path),
        "card_path": str(card_result.metrics["card_artifact_path"]),
    }


def _card_for_uid(rows: list[dict[str, Any]], uid: str) -> dict[str, Any]:
    for row in rows:
        if row.get("uid") == uid:
            card = read_json(str(row.get("telegram_card_artifact") or ""), {})
            if card:
                return card
    raise FileNotFoundError(f"card not found for uid={uid}")


def _click(
    handler: OperatorBotHandler,
    card: dict[str, Any],
    action: str,
    client: "FakeTelegramClient",
    *,
    callback_id: str,
) -> dict[str, Any]:
    callback_data = _callback_data(card, action)
    return handler.handle_callback(
        callback_data=callback_data,
        chat_id=card["telegram_chat_id"],
        message_id=int(card["telegram_message_id"]),
        operator_telegram_id="101",
        operator_username="demo_operator",
        callback_query_id=callback_id,
    )


def _callback_data(card: dict[str, Any], action: str) -> str:
    for item in card.get("keyboard") or []:
        if isinstance(item, dict) and item.get("action") == action:
            return str(item.get("callback_data") or "")
    raise KeyError(f"callback action missing: {action}")


def _record(checks: list[dict[str, Any]], name: str, passed: bool, note: str = "") -> None:
    checks.append({"name": name, "passed": bool(passed), "note": note or ("ok" if passed else "failed")})


class FakeTelegramClient:
    def __init__(self) -> None:
        self.operations: list[dict[str, Any]] = []
        self.next_message_id = 9000

    def send_message(
        self,
        *,
        chat_id: str | int,
        text: str,
        reply_markup: dict[str, Any] | None = None,
        reply_to_message_id: int | str | None = None,
    ) -> dict[str, Any]:
        self.next_message_id += 1
        return self._ok(
            "sendMessage",
            chat_id=chat_id,
            message_id=self.next_message_id,
            text=text,
            reply_markup=reply_markup or {},
            reply_to_message_id=reply_to_message_id,
        )

    def edit_message_text(
        self,
        *,
        chat_id: str | int,
        message_id: int,
        text: str,
        reply_markup: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self._ok("editMessageText", chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup or {})

    def edit_message_reply_markup(
        self,
        *,
        chat_id: str | int,
        message_id: int,
        reply_markup: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self._ok("editMessageReplyMarkup", chat_id=chat_id, message_id=message_id, reply_markup=reply_markup or {})

    def answer_callback_query(self, *, callback_query_id: str, text: str = "") -> dict[str, Any]:
        return self._ok("answerCallbackQuery", callback_query_id=callback_query_id, text=text)

    def delete_message(self, *, chat_id: str | int, message_id: int | str) -> dict[str, Any]:
        return self._ok("deleteMessage", chat_id=chat_id, message_id=int(message_id))

    def send_photo(self, *, chat_id: str | int, photo_path: str, caption: str = "") -> dict[str, Any]:
        self.next_message_id += 1
        return self._ok("sendPhoto", chat_id=chat_id, message_id=self.next_message_id, file_path=photo_path, caption=caption)

    def send_document(self, *, chat_id: str | int, document_path: str, caption: str = "") -> dict[str, Any]:
        self.next_message_id += 1
        return self._ok("sendDocument", chat_id=chat_id, message_id=self.next_message_id, file_path=document_path, caption=caption)

    def _ok(self, operation: str, **payload: Any) -> dict[str, Any]:
        result = {"operation": operation, "ok": True, **payload}
        self.operations.append(result)
        return result


def _render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Flow acceptance smoke",
        "",
        f"- status: {report['status']}",
        f"- created_at: {report['created_at']}",
        f"- fake_telegram_callbacks: {report['fake_telegram_callbacks']['status']}",
        "",
        "| UID | source | class | enrichment | KB | draft | pass | notes |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in report["rows"]:
        notes = "; ".join(str(item) for item in row.get("notes") or [])
        lines.append(
            "| {uid} | {source} | {cls} | {enrich} | {kb} | {draft} | {passed} | {notes} |".format(
                uid=row["uid"],
                source=row["source_status"],
                cls=row["classification"] or "-",
                enrich=row["enrichment_status"] or "-",
                kb=row["knowledge_status"] or "-",
                draft=row["draft_status"] or "-",
                passed="yes" if row["passed"] else "no",
                notes=notes.replace("|", "/"),
            )
        )
    lines.extend(["", "## Fake Telegram callbacks", ""])
    for check in report["fake_telegram_callbacks"]["checks"]:
        status = "passed" if check["passed"] else "failed"
        lines.append(f"- {check['name']}: {status} ({check['note']})")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
