from __future__ import annotations

import html
import hashlib
import json
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any

from src.pipeline.early_classification import early_classification
from src.shared.common.message_dossier import load_message_record, write_message_dossier
from src.shared.common.paths import resolve_project_path


CARD_TITLE = "📩 Новое письмо"
CALLBACK_PREFIX = "ma"
TELEGRAM_CHAT_ID_MOCK = "mock-operator-chat"


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def timestamp_for_filename(moment: datetime | None = None) -> str:
    value = moment or now_utc()
    return value.strftime("%Y%m%dT%H%M%S%f")


def read_json(path: str | Path, default: Any) -> Any:
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = resolve_project_path(file_path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: str | Path, payload: Any) -> str:
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = resolve_project_path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(file_path)


def resolve_dossier_input(dossier_path: str | None, context_artifacts: dict[str, list[str]] | None = None) -> Path | None:
    if dossier_path:
        return resolve_project_path(dossier_path)

    for refs in (context_artifacts or {}).values():
        for ref in reversed(refs):
            candidate = resolve_project_path(ref)
            if candidate.suffix.lower() == ".md" and candidate.exists():
                return candidate
    return None


def load_dossier(path: str | Path) -> dict[str, Any]:
    payload = load_message_record(path)
    if not isinstance(payload, dict):
        raise ValueError("Dossier payload must be an object")
    return payload


def save_dossier(path: str | Path, payload: dict[str, Any]) -> str:
    return write_message_dossier(path, payload)


def resolve_uid(payload: dict[str, Any]) -> str:
    metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
    for key in ("uid", "fixture_ref"):
        value = str(metadata.get(key, "") or "").strip()
        if value:
            return value
    for module_name in ("case_thread_binding", "identity_context_enrichment", "draft_builder"):
        module = (payload.get("modules") or {}).get(module_name) or {}
        value = str(module.get("uid", "") or "").strip()
        if value and value != "unknown":
            return value
    return str(payload.get("uid", "") or "unknown")


def headers(payload: dict[str, Any]) -> dict[str, Any]:
    value = payload.get("headers") or {}
    return value if isinstance(value, dict) else {}


def modules(payload: dict[str, Any]) -> dict[str, Any]:
    value = payload.setdefault("modules", {})
    if not isinstance(value, dict):
        value = {}
        payload["modules"] = value
    return value


def case_binding(payload: dict[str, Any]) -> dict[str, Any]:
    value = (payload.get("modules") or {}).get("case_thread_binding") or {}
    return value if isinstance(value, dict) else {}


def enrichment_module(payload: dict[str, Any]) -> dict[str, Any]:
    value = (payload.get("modules") or {}).get("identity_context_enrichment") or {}
    return value if isinstance(value, dict) else {}


def enrichment_result(payload: dict[str, Any]) -> dict[str, Any]:
    value = enrichment_module(payload).get("result") or {}
    return value if isinstance(value, dict) else {}


def llm_output(payload: dict[str, Any]) -> dict[str, Any]:
    value = ((payload.get("modules") or {}).get("llm_understanding") or {}).get("structured_output") or {}
    return value if isinstance(value, dict) else {}


def knowledge_retrieval(payload: dict[str, Any]) -> dict[str, Any]:
    value = (payload.get("modules") or {}).get("knowledge_retrieval") or {}
    return value if isinstance(value, dict) else {}


def decision_layer(payload: dict[str, Any]) -> dict[str, Any]:
    value = (payload.get("modules") or {}).get("decision_layer") or {}
    return value if isinstance(value, dict) else {}


def case_id(payload: dict[str, Any]) -> str:
    return str(case_binding(payload).get("case_id", "") or "case-unknown")


def thread_id(payload: dict[str, Any]) -> str:
    return str(case_binding(payload).get("thread_id", "") or "thread-unknown")


def subject(payload: dict[str, Any]) -> str:
    return str(headers(payload).get("subject", "") or "").strip()


def sender(payload: dict[str, Any]) -> str:
    return str(headers(payload).get("sender", "") or "").strip()


def response_mode(payload: dict[str, Any]) -> str:
    decision = decision_layer(payload)
    llm = llm_output(payload)
    return str(
        decision.get("response_mode_final")
        or decision.get("response_mode_initial")
        or llm.get("response_mode")
        or "ask_clarifying_question"
    )


def latest_draft_module(payload: dict[str, Any]) -> dict[str, Any]:
    value = (payload.get("modules") or {}).get("draft_builder") or {}
    return value if isinstance(value, dict) else {}


def draft_revisions(payload: dict[str, Any]) -> list[dict[str, Any]]:
    draft = latest_draft_module(payload)
    revisions = draft.get("revisions")
    if isinstance(revisions, list) and revisions:
        return [item for item in revisions if isinstance(item, dict)]
    legacy_text = str(draft.get("draft_text", "") or "").strip()
    if not legacy_text:
        return []
    return [
        {
            "revision": int(draft.get("latest_revision") or 0),
            "draft_text": legacy_text,
            "operator_comment": "",
            "created_at": str(draft.get("created_at", "") or ""),
            "revision_reason": "legacy",
        }
    ]


def latest_draft_text(payload: dict[str, Any]) -> str:
    revisions = draft_revisions(payload)
    if revisions:
        return str(revisions[-1].get("draft_text", "") or "").strip()
    return str(latest_draft_module(payload).get("draft_text", "") or "").strip()


def latest_action_suggestion(payload: dict[str, Any]) -> dict[str, Any]:
    module = modules(payload).get("action_suggestion_builder")
    if isinstance(module, dict):
        revisions = module.get("revisions")
        if isinstance(revisions, list) and revisions:
            latest = revisions[-1]
            if isinstance(latest, dict):
                return latest
        text = str(module.get("action_text") or "").strip()
        if text:
            return {
                "revision": int(module.get("latest_revision") or 1),
                "action_type": str(module.get("action_type") or ""),
                "action_text": text,
                "operator_comment": str(module.get("operator_comment") or ""),
            }
    return _base_action_suggestion(payload)


def build_action_suggestion_revision(
    payload: dict[str, Any],
    *,
    dossier_path: str,
    operator_comment: str = "",
    revision_reason: str = "operator_needs_edit_comment",
) -> dict[str, Any]:
    existing_module = modules(payload).get("action_suggestion_builder")
    existing = []
    if isinstance(existing_module, dict) and isinstance(existing_module.get("revisions"), list):
        existing = [item for item in existing_module["revisions"] if isinstance(item, dict)]
    base = latest_action_suggestion(payload)
    revision = len(existing) + 1
    comment = " ".join(operator_comment.split()).strip()
    action_text = str(base.get("action_text") or "").strip() or "Кейс помечен для ручной обработки. Реальная маршрутизация пока не подключена."
    if comment:
        action_text = f"{action_text}\nУточнение оператора: {comment}"
    revision_payload = {
        "revision": revision,
        "created_at": now_utc().isoformat(),
        "revision_reason": revision_reason,
        "operator_comment": comment,
        "action_type": str(base.get("action_type") or ""),
        "action_text": action_text,
    }
    revisions = existing + [revision_payload]
    module_payload = {
        "uid": resolve_uid(payload),
        "status": "ok",
        "error": "",
        "latest_revision": revision,
        "action_type": revision_payload["action_type"],
        "action_text": action_text,
        "operator_comment": comment,
        "created_at": revision_payload["created_at"],
        "dossier_path": dossier_path,
        "revisions": revisions,
    }
    modules(payload)["action_suggestion_builder"] = module_payload
    return module_payload


def _base_action_suggestion(payload: dict[str, Any]) -> dict[str, Any]:
    decision = decision_layer(payload)
    early = early_classification(payload)
    return {
        "revision": 0,
        "action_type": str(decision.get("proposed_action_type") or early.get("proposed_action_type") or "").strip(),
        "action_text": str(decision.get("proposed_action_text") or early.get("proposed_action_text") or "").strip(),
        "operator_comment": "",
    }


def build_draft_revision(
    payload: dict[str, Any],
    *,
    dossier_path: str,
    operator_comment: str = "",
    revision_reason: str = "initial",
) -> dict[str, Any]:
    existing = draft_revisions(payload)
    clean_operator_comment = operator_comment.strip()
    skip_reason = _draft_skip_reason(payload)
    # Base draft is version 0. Operator comments create v1/v2/...
    # If the initial case is skipped, keep it skipped until an operator comment arrives.
    if skip_reason and not clean_operator_comment:
        draft_payload = {
            "uid": resolve_uid(payload),
            "status": "skipped",
            "error": "",
            "skip_reason": skip_reason,
            "draft_type": response_mode(payload),
            "latest_revision": _latest_draft_revision_number(existing),
            "draft_text": "",
            "operator_note": skip_reason,
            "source_response_mode": response_mode(payload),
            "created_at": now_utc().isoformat(),
            "dossier_path": dossier_path,
            "revisions": existing,
            "inputs": {
                "llm_understanding_status": str(((payload.get("modules") or {}).get("llm_understanding") or {}).get("status", "") or ""),
                "knowledge_retrieval_status": str(knowledge_retrieval(payload).get("status", "") or ""),
                "decision_layer_status": str(decision_layer(payload).get("status", "") or ""),
                "knowledge_item_ids": [],
            },
        }
        modules(payload)["draft_builder"] = draft_payload
        return draft_payload
    revision = _next_draft_revision_number(existing, has_operator_comment=bool(clean_operator_comment))
    mode = response_mode(payload)
    if clean_operator_comment and skip_reason and mode in {"no_reply", "ignore", "handoff_to_operator"}:
        mode = "operator_revision"
    draft_text = _build_draft_text(payload, mode=mode, operator_comment=operator_comment, prior_text=latest_draft_text(payload))
    created_at = now_utc().isoformat()
    revision_payload = {
        "revision": revision,
        "created_at": created_at,
        "revision_reason": revision_reason,
        "operator_comment": operator_comment.strip(),
        "draft_type": mode,
        "draft_text": draft_text,
    }
    revisions = existing + [revision_payload]
    draft_payload = {
        "uid": resolve_uid(payload),
        "status": "ok",
        "error": "",
        "draft_type": mode,
        "latest_revision": revision,
        "draft_text": draft_text,
        "operator_note": "Черновик создан в демо-режиме; реальная отправка отключена.",
        "source_response_mode": mode,
        "created_at": created_at,
        "dossier_path": dossier_path,
        "revisions": revisions,
        "inputs": {
            "llm_understanding_status": str(((payload.get("modules") or {}).get("llm_understanding") or {}).get("status", "") or ""),
            "knowledge_retrieval_status": str(knowledge_retrieval(payload).get("status", "") or ""),
            "decision_layer_status": str(decision_layer(payload).get("status", "") or ""),
            "knowledge_item_ids": [str(item.get("id", "") or "") for item in _knowledge_items(payload) if item.get("id")],
        },
    }
    modules(payload)["draft_builder"] = draft_payload
    return draft_payload


def render_operator_card(
    payload: dict[str, Any],
    *,
    status_notice: str = "",
    action: str = "",
) -> str:
    lines: list[str] = [f"<b>{_e(CARD_TITLE)}</b>"]
    if status_notice:
        lines.extend(["", _e(status_notice)])

    lines.extend(
        [
            "",
            "<b>Письмо</b>",
            f"UID: {_e(resolve_uid(payload))}",
            f"Получено: {_e(_received_at_display(payload))}",
            f"От: {_e(sender(payload) or '<empty>')}",
            f"Тема письма: {_e(subject(payload) or 'без темы')}",
            f"Суть обращения: {_e(_message_brief(payload))}",
            "",
            "<b>Кейс</b>",
            f"Case ID: {_e(case_id(payload))} · Thread ID: {_e(thread_id(payload))}",
        ]
    )

    lines.extend(["", "<b>История переписки</b>"])
    lines.extend(_render_thread_history(payload))
    lines.extend(["", "<b>Вложения</b>"])
    lines.extend(_render_attachments(payload))
    lines.extend(["", "<b>Проверка билетов / Enrichment</b>", _e(_compact_enrichment(payload))])
    lines.extend(["", "<b>Что понял ассистент</b>"])
    lines.extend(_render_understanding(payload))
    lines.extend(["", "<b>Предлагаемое решение</b>"])
    lines.extend(_render_decision(payload))
    action_lines = _render_proposed_action(payload)
    if action_lines:
        lines.extend(["", "<b>Предлагаемое действие</b>"])
        lines.extend(action_lines)
    lines.extend(["", "<b>База знаний</b>"])
    lines.extend(_render_knowledge(payload))
    lines.extend(["", "<b>Что не хватает</b>"])
    lines.extend(_render_list(decision_layer(payload).get("missing_data") or []))
    lines.extend(["", "<b>Риски</b>"])
    lines.extend(_render_list(decision_layer(payload).get("risks") or []))

    for idx, operator_comment in enumerate(_operator_comment_revisions(payload), start=1):
        lines.extend(["", f"<b>Комментарий оператора v{idx}</b>", _e(operator_comment)])

    draft_text = latest_draft_text(payload)
    latest_revision = _latest_draft_revision_number(draft_revisions(payload))
    if draft_text:
        lines.extend(["", f"<b>Черновик v{_e(str(latest_revision))}</b>"])
        lines.append(_e(draft_text))
    else:
        lines.extend(["", "<b>Черновик</b>"])
        lines.append(_e(_draft_skip_reason(payload) or "Черновик не создавался: ответ клиенту не требуется."))

    if action:
        lines.extend(["", f"<b>Последнее действие</b>", _e(_action_label(action))])

    return "\n".join(lines)



def _operator_comment_revisions(payload: dict[str, Any]) -> list[str]:
    comments: list[str] = []
    seen: set[str] = set()

    def add(raw: Any) -> None:
        comment = " ".join(str(raw or "").split()).strip()
        if not comment or comment in seen:
            return
        seen.add(comment)
        comments.append(comment)

    modules_payload = payload.get("modules") or {}
    revision_requests = modules_payload.get("revision_requests") if isinstance(modules_payload.get("revision_requests"), dict) else {}
    requests = revision_requests.get("requests") if isinstance(revision_requests, dict) else []
    if isinstance(requests, list):
        for item in requests:
            if isinstance(item, dict):
                add(item.get("operator_comment"))
    latest_request = revision_requests.get("latest_request") if isinstance(revision_requests, dict) else {}
    if isinstance(latest_request, dict):
        add(latest_request.get("operator_comment"))

    for item in draft_revisions(payload):
        add(item.get("operator_comment"))

    action_module = modules_payload.get("action_suggestion_builder") if isinstance(modules_payload.get("action_suggestion_builder"), dict) else {}
    revisions = action_module.get("revisions") if isinstance(action_module, dict) else []
    if isinstance(revisions, list):
        for item in revisions:
            if isinstance(item, dict):
                add(item.get("operator_comment"))
    if isinstance(action_module, dict):
        add(action_module.get("operator_comment"))

    return comments


def _operator_draft_revision_count(revisions: list[dict[str, Any]]) -> int:
    return sum(1 for item in revisions if str(item.get("operator_comment") or "").strip())


def _next_draft_revision_number(revisions: list[dict[str, Any]], *, has_operator_comment: bool) -> int:
    if has_operator_comment:
        return _operator_draft_revision_count(revisions) + 1
    return 0


def _latest_draft_revision_number(revisions: list[dict[str, Any]]) -> int:
    if not revisions:
        return 0
    latest = revisions[-1]
    try:
        return int(latest.get("revision") or 0)
    except (TypeError, ValueError):
        return _operator_draft_revision_count(revisions)

def persist_operator_card(
    payload: dict[str, Any],
    *,
    dossier_path: str,
    artifacts_dir: str,
    card_text: str,
    card_status: str,
    action: str = "",
    telegram_message_id: int | str | None = None,
    telegram_chat_id: int | str | None = None,
    telegram_delivery_mode: str = "artifact_only",
    telegram_operations: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    base_dir = resolve_project_path(artifacts_dir)
    state_dir = base_dir / "state"
    state_dir.mkdir(parents=True, exist_ok=True)
    message_id = telegram_message_id
    if message_id is None:
        message_id = _next_mock_message_id(state_dir / "operator_bot_state.json")
    chat_id = telegram_chat_id if telegram_chat_id is not None else TELEGRAM_CHAT_ID_MOCK
    created_at = now_utc().isoformat()
    callbacks = build_callbacks(payload)
    card_payload = {
        "uid": resolve_uid(payload),
        "status": card_status,
        "error": "",
        "created_at": created_at,
        "dossier_path": dossier_path,
        "source_dossier_path": dossier_path,
        "case_id": case_id(payload),
        "thread_id": thread_id(payload),
        "telegram_message_id": message_id,
        "telegram_chat_id": chat_id,
        "telegram_delivery_mode": telegram_delivery_mode,
        "telegram_operations": telegram_operations or [],
        "callback_data": [item["callback_data"] for item in callbacks],
        "keyboard": callbacks,
        "card_text": card_text,
        "action": action,
        "artifacts_dir": artifacts_dir,
    }
    card_dir = base_dir / "telegram_operator_delivery" / case_id(payload)
    card_path = card_dir / f"card_{timestamp_for_filename()}.json"
    card_payload["card_artifact_path"] = write_json(card_path, card_payload)
    _append_card_index(base_dir / "state" / "operator_cards_index.json", card_payload)
    modules(payload)["telegram_operator_delivery"] = card_payload
    return card_payload


def build_callbacks(payload: dict[str, Any]) -> list[dict[str, str]]:
    token = _callback_token(payload)
    labels = {
        "approve": "✅ Утвердить",
        "needs_edit": "✏️ На доработку (LLM)",
        "handoff": "👤 Оператору",
        "ignore": "🚫 Игнорировать",
    }
    if _has_proposed_action(payload):
        labels["action_request"] = "⚡ Выполнить действие"
    return [
        {
            "action": action,
            "label": label,
            "callback_data": f"{CALLBACK_PREFIX}|{action}|{token}",
        }
        for action, label in labels.items()
    ]


def build_reply_markup(payload: dict[str, Any]) -> dict[str, Any]:
    callbacks = build_callbacks(payload)
    first = callbacks[:2]
    second = callbacks[2:4]
    third = callbacks[4:]
    keyboard = []
    if first:
        keyboard.append([{"text": item["label"], "callback_data": item["callback_data"]} for item in first])
    if second:
        keyboard.append([{"text": item["label"], "callback_data": item["callback_data"]} for item in second])
    if third:
        keyboard.append([{"text": item["label"], "callback_data": item["callback_data"]} for item in third])
    return {
        "inline_keyboard": keyboard
    }


def parse_callback_data(callback_data: str) -> dict[str, str]:
    parts = str(callback_data or "").split("|")
    if len(parts) == 3 and parts[0] == CALLBACK_PREFIX:
        return {
            "action": parts[1],
            "uid": "",
            "case_id": "",
            "thread_id": "",
            "token": parts[2],
        }
    if len(parts) != 5 or parts[0] != CALLBACK_PREFIX:
        raise ValueError("Invalid callback_data")
    return {
        "action": parts[1],
        "uid": parts[2],
        "case_id": parts[3],
        "thread_id": parts[4],
        "token": "",
    }


def find_dossier_from_card_index(artifacts_dir: str, callback_data: str) -> str:
    parsed = parse_callback_data(callback_data)
    index_path = resolve_project_path(artifacts_dir) / "state" / "operator_cards_index.json"
    index = read_json(index_path, {"cards": []})
    cards = index.get("cards") if isinstance(index, dict) else []
    if not isinstance(cards, list):
        cards = []
    for card in reversed(cards):
        if not isinstance(card, dict):
            continue
        callback_items = card.get("callback_data") or []
        if isinstance(callback_items, list) and callback_data in callback_items:
            dossier = str(card.get("source_dossier_path") or card.get("dossier_path") or "").strip()
            if dossier:
                return dossier
        if not parsed.get("uid"):
            continue
        if str(card.get("uid", "")) != parsed["uid"]:
            continue
        if str(card.get("case_id", "")) != parsed["case_id"]:
            continue
        dossier = str(card.get("source_dossier_path") or card.get("dossier_path") or "").strip()
        if dossier:
            return dossier
    raise FileNotFoundError("No card index entry found for callback_data")


def _callback_token(payload: dict[str, Any]) -> str:
    raw = f"{resolve_uid(payload)}|{case_id(payload)}|{thread_id(payload)}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def action_status_notice(
    action: str,
    *,
    mock_refs: list[str] | None = None,
    payload: dict[str, Any] | None = None,
) -> str:
    if action == "approve":
        if mock_refs:
            return "✅ Статус: утверждено\nMock-ответ создан.\nРеальный email не отправлен."
        return "✅ Статус: утверждение не выполнено\nЧерновик отсутствует, mock-ответ не создан."
    if action == "needs_edit":
        if payload is not None and not latest_draft_text(payload) and _has_proposed_action(payload):
            return "✏️ Предложенное действие обновлено по комментарию оператора."
        return "✏️ Черновик доработан LLM по комментарию оператора."
    if action == "handoff":
        return "👤 Кейс помечен для ручной обработки. Реальная маршрутизация пока не подключена."
    if action == "ignore":
        reason = _ignore_reason(payload or {})
        return f"🚫 Ответ не требуется: кейс закрыт как {reason}."
    if action == "action_request":
        return f"⚡ Действие зафиксировано: {_action_request_result_text(payload or {})}"
    return "Действие оператора обработано.\nРеальный email не отправлен."


def needs_edit_waiting_notice() -> str:
    return (
        "✏️ Статус: ожидается комментарий для доработки LLM\n"
        "Напиши следующим сообщением, что нужно исправить в карточке/черновике."
    )


def _build_draft_text(payload: dict[str, Any], *, mode: str, operator_comment: str, prior_text: str) -> str:
    comment = operator_comment.strip()
    if comment and prior_text:
        return _revise_draft(prior_text, comment)
    if comment and not prior_text:
        return _draft_from_operator_comment(payload, comment)

    decision = decision_layer(payload)
    llm = llm_output(payload)
    missing = [str(item).strip() for item in decision.get("missing_data") or [] if str(item).strip()]
    knowledge_lines = _knowledge_template_lines(payload)
    need = str(llm.get("customer_need", "") or "обращение").strip()

    if mode in {"no_reply", "ignore"}:
        reason = str(decision.get("decision_reason") or llm.get("response_mode_reason") or "Ответ не требуется").strip()
        return reason

    if mode == "handoff_to_operator":
        return "Кейс помечен для ручной обработки. Реальная маршрутизация пока не подключена."

    lines = ["Здравствуйте."]
    if mode == "ask_clarifying_question":
        lines.append(f"Чтобы корректно обработать обращение ({need}), пожалуйста, уточните:")
        if missing:
            lines.extend(f"- {item}" for item in missing)
        else:
            lines.append("- номер заказа, телефон или email, указанный при покупке.")
    else:
        summary = str(llm.get("summary", "") or need).strip()
        lines.append(summary)

    lines.extend(knowledge_lines)
    lines.append("После этого мы сможем продолжить проверку.")
    lines.append("С уважением, команда mooon.")
    return "\n".join(line for line in lines if line.strip())


def _draft_from_operator_comment(payload: dict[str, Any], operator_comment: str) -> str:
    instruction = _clean_operator_revision_instruction(operator_comment)
    lines = ["Здравствуйте."]
    if instruction:
        # Ветка "На доработку (LLM)": комментарий оператора — это инструкция,
        # а не текст, который нужно механически вставить в черновик.
        lines.append(_sentence(instruction))
    else:
        need = str(llm_output(payload).get("customer_need", "") or "обращение").strip()
        lines.append(f"Мы проверим ваше обращение: {need}.")
    lines.append("С уважением, команда mooon.")
    return "\n".join(line for line in lines if line.strip())


def _revise_draft(prior_text: str, operator_comment: str) -> str:
    text = prior_text.strip()
    instruction = _clean_operator_revision_instruction(operator_comment)
    lowered = instruction.casefold()
    if not instruction:
        return text

    # Ветка "На доработку (LLM)": используем комментарий как инструкцию для
    # уточнения черновика. Не добавляем "Комментарий 1/2" и не вставляем сырую
    # команду оператора в письмо клиенту.
    if _asks_for_shorter_or_clearer(lowered):
        core_lines = [line.strip() for line in text.splitlines() if line.strip()]
        signature = "С уважением, команда mooon."
        core_lines = [line for line in core_lines if line != signature]
        body = " ".join(core_lines[1:] if core_lines and core_lines[0].lower().startswith("здравствуйте") else core_lines)
        if not body:
            body = instruction
        return "\n".join(
            [
                "Здравствуйте.",
                _sentence(_compact_sentence(body)),
                signature,
            ]
        )

    if lowered.startswith(("убери ", "удали ", "не пиши ")):
        removal = re.sub(r"^(убери|удали|не пиши)\s+", "", instruction, flags=re.IGNORECASE).strip(" .:;")
        if removal:
            lines = [line for line in text.splitlines() if removal.casefold() not in line.casefold()]
            return "\n".join(line for line in lines if line.strip()) or text
        return text

    addition = _sentence(instruction)
    if _line_exists(text, addition):
        return text

    signature = "С уважением, команда mooon."
    if signature in text:
        return text.replace(signature, f"{addition}\n{signature}")
    return f"{text}\n{addition}"


def _clean_operator_revision_instruction(operator_comment: str) -> str:
    comment = " ".join(str(operator_comment or "").split()).strip()
    lowered = comment.casefold()
    prefixes = [
        "добавь в ответ:",
        "добавь в черновик:",
        "добавь:",
        "напиши:",
        "ответь:",
        "укажи:",
        "исправь:",
        "перепиши:",
        "сделай:",
    ]
    for prefix in prefixes:
        if lowered.startswith(prefix):
            return comment[len(prefix):].strip(" .:-")
    return comment


def _asks_for_shorter_or_clearer(lowered_instruction: str) -> bool:
    return any(token in lowered_instruction for token in ["короче", "мягче", "понятнее", "проще", "человечнее"])


def _sentence(value: str) -> str:
    text = " ".join(str(value or "").split()).strip()
    if not text:
        return ""
    text = text[:1].upper() + text[1:]
    if text[-1:] not in {".", "!", "?"}:
        text += "."
    return text


def _compact_sentence(value: str) -> str:
    text = " ".join(str(value or "").split()).strip()
    if len(text) <= 260:
        return text
    return text[:257].rstrip() + "..."


def _line_exists(text: str, line: str) -> bool:
    target = " ".join(line.casefold().split()).strip()
    for existing in text.splitlines():
        if " ".join(existing.casefold().split()).strip() == target:
            return True
    return False


def _knowledge_template_lines(payload: dict[str, Any]) -> list[str]:
    if knowledge_retrieval(payload).get("status") == "skipped":
        return []
    lines: list[str] = []
    for item in _knowledge_items(payload)[:3]:
        if _is_irrelevant_knowledge_item(payload, item):
            continue
        hint = str(item.get("template_hint") or item.get("operator_instruction") or item.get("content") or "").strip()
        if hint:
            lines.append(hint)
    return lines


def _knowledge_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    value = knowledge_retrieval(payload).get("matched_items") or []
    return [item for item in value if isinstance(item, dict)]


def _display_knowledge_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [item for item in _knowledge_items(payload) if not _is_irrelevant_knowledge_item(payload, item)]


def _is_irrelevant_knowledge_item(payload: dict[str, Any], item: dict[str, Any]) -> bool:
    body = " ".join(
        str(value or "")
        for value in [
            subject(payload),
            payload.get("body_text"),
            _message_brief(payload),
        ]
    ).casefold()
    is_payment_error = "ошибка" in body and ("оплат" in body or "платеж" in body or "платёж" in body)
    if not is_payment_error:
        return False
    item_text = " ".join(
        str(item.get(key) or "")
        for key in ("id", "title", "content", "operator_instruction", "template_hint")
    ).casefold()
    irrelevant_tokens = ["обмен", "возврат", "потерял", "потерян", "нет чека", "lost"]
    return any(token in item_text for token in irrelevant_tokens) and not any(
        token in body for token in ["возврат", "вернуть", "потерял", "потерян", "не приш"]
    )


def _routing_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    value = knowledge_retrieval(payload).get("routing_matches") or []
    return [item for item in value if isinstance(item, dict)]


def _has_proposed_action(payload: dict[str, Any]) -> bool:
    suggestion = latest_action_suggestion(payload)
    action_type = str(suggestion.get("action_type") or "").strip()
    action_text = str(suggestion.get("action_text") or "").strip()
    return bool(action_type and action_text)


def _render_proposed_action(payload: dict[str, Any]) -> list[str]:
    suggestion = latest_action_suggestion(payload)
    text = str(suggestion.get("action_text") or "").strip()
    if not text:
        return []
    action_type = _human_action_type(str(suggestion.get("action_type") or "").strip())
    lines = [_e(text)]
    latest_revision = int(suggestion.get("revision") or 0)
    if latest_revision > 0:
        lines.insert(0, f"Версия предложения: v{latest_revision}")
    if action_type:
        lines.append(f"Тип действия: {_e(action_type)}")
    return lines


def _draft_skip_reason(payload: dict[str, Any]) -> str:
    draft = latest_draft_module(payload)
    explicit = str(draft.get("skip_reason") or "").strip()
    if explicit:
        return explicit
    early = early_classification(payload)
    if early and early.get("should_build_customer_draft") is False:
        classification = str(early.get("classification") or "")
        if classification in {"newsletter_or_promo", "security_or_no_reply_noise", "bounce_or_delivery_noise", "gratitude_or_case_closed"}:
            return "Черновик не создавался: ответ клиенту не требуется."
        if classification == "action_required_notification":
            return "Черновик не создавался: это служебное уведомление, нужен только внутренний action."
        if classification == "schedule_or_repertoire_question":
            return "Черновик не создавался: вопрос требует проверки расписания/репертуара ответственными."
        if classification in {"business_proposal", "candidate_or_portfolio", "training_invitation"}:
            return "Черновик не создавался: обращение помечено для ручной обработки ответственными."
        return "Черновик не создавался: клиентский ответ не требуется на этом шаге."
    if response_mode(payload) in {"no_reply", "ignore"}:
        return "Черновик не создавался: ответ клиенту не требуется."
    return ""


def _compact_enrichment(payload: dict[str, Any]) -> str:
    result = enrichment_result(payload)
    resolved = result.get("resolved_match") or {}
    status = str(result.get("ticket_db_status") or "").strip() or "нет данных"
    note = str(result.get("note") or "").strip()
    if status == "skipped":
        return "Проверка билетов: не запускалась — письмо не похоже на клиентский билетный вопрос."
    if status == "unavailable":
        detail = f" — {note}" if note else ""
        return f"Проверка билетов: временно недоступна{detail}."
    if status == "error":
        detail = f" — {note}" if note else ""
        return f"Проверка билетов: ошибка{detail}."
    if isinstance(resolved, dict) and resolved:
        return f"Билет найден: {_compact_ticket(resolved)}"
    if status in {"found_strict", "rescue_candidates"} and note:
        return f"Билет: не найден\nКомментарий: {note}"
    return "Билет: не найден"


def _compact_ticket(ticket: dict[str, Any]) -> str:
    parts = [
        f"Билет #{ticket.get('ticket')}" if ticket.get("ticket") else "Билет найден",
        f"заказ {ticket.get('idTrading')}" if ticket.get("idTrading") else "",
        str(ticket.get("event") or ""),
        " ".join(str(ticket.get(key) or "") for key in ("dateShow", "timeShow")).strip(),
        str(ticket.get("theater") or ""),
    ]
    return " · ".join(part for part in parts if part)


def _received_at_display(payload: dict[str, Any]) -> str:
    for value in _received_header_dates(payload):
        parsed = _parse_mail_datetime(value)
        if parsed is not None:
            return parsed.strftime("%d.%m.%Y %H:%M")
    sent_at = str(headers(payload).get("sent_at") or "").strip()
    parsed = _parse_mail_datetime(sent_at)
    if parsed is not None:
        return parsed.strftime("%d.%m.%Y %H:%M")
    return now_utc().strftime("%d.%m.%Y %H:%M")


def _received_header_dates(payload: dict[str, Any]) -> list[str]:
    raw = str(payload.get("raw_headers") or "")
    if not raw:
        return []
    values: list[str] = []
    current_name = ""
    current_value = ""
    for line in raw.splitlines():
        if line[:1] in {" ", "\t"} and current_name:
            current_value += " " + line.strip()
            continue
        if current_name.lower() == "received":
            values.append(current_value)
        if ":" not in line:
            current_name = ""
            current_value = ""
            continue
        current_name, current_value = line.split(":", 1)
        current_name = current_name.strip()
        current_value = current_value.strip()
    if current_name.lower() == "received":
        values.append(current_value)
    dates = []
    for value in values:
        if ";" in value:
            dates.append(value.rsplit(";", 1)[-1].strip())
    return dates


def _parse_mail_datetime(value: str) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return parsedate_to_datetime(text)
    except Exception:
        pass
    candidates = [text]
    if text.endswith("Z"):
        candidates.append(text[:-1] + "+00:00")
    if "T" not in text and " " in text:
        candidates.append(text.replace(" ", "T", 1))
    for candidate in candidates:
        try:
            parsed = datetime.fromisoformat(candidate)
            if parsed.tzinfo is None:
                return parsed.replace(tzinfo=timezone.utc)
            return parsed
        except Exception:
            continue
    return None


def _render_attachments(payload: dict[str, Any]) -> list[str]:
    items = _attachment_items(payload)
    if not items:
        return ["нет"]
    lines = [f"Файлов: {len(items)}"]
    for item in items[:6]:
        name = str(item.get("filename_original") or item.get("filename") or item.get("filename_saved") or "файл").strip()
        content_type = str(item.get("content_type") or "").strip()
        type_label = _attachment_type_label(content_type, name)
        meaning = _attachment_meaning(payload, item)
        lines.append(f"- {_e(name)} · {_e(type_label)} · {_e(meaning)}")
    if len(items) > 6:
        lines.append(f"- ещё файлов: {len(items) - 6}")
    return lines


def _attachment_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    module = (payload.get("modules") or {}).get("attachment_extraction") or {}
    items = module.get("items") if isinstance(module, dict) else []
    if isinstance(items, list) and items:
        return [item for item in items if isinstance(item, dict)]
    inventory = payload.get("attachments_inventory") or []
    return [item for item in inventory if isinstance(item, dict)]


def _attachment_type_label(content_type: str, name: str) -> str:
    value = str(content_type or "").lower()
    suffix = Path(name or "").suffix.lower()
    if value in {"image/png"} or suffix == ".png":
        return "изображение PNG"
    if value in {"image/jpeg", "image/jpg"} or suffix in {".jpg", ".jpeg"}:
        return "изображение JPEG"
    if value == "image/webp" or suffix == ".webp":
        return "изображение WebP"
    if value.startswith("image/"):
        return "изображение"
    if value == "application/pdf" or suffix == ".pdf":
        return "PDF"
    if suffix == ".docx":
        return "DOCX"
    if suffix in {".xls", ".xlsx", ".csv"}:
        return "таблица"
    if suffix in {".doc", ".docx", ".rtf", ".txt"}:
        return "документ"
    return "файл"


def _attachment_meaning(payload: dict[str, Any], item: dict[str, Any]) -> str:
    name = str(item.get("filename_original") or item.get("filename") or item.get("filename_saved") or "").casefold()
    body = " ".join([subject(payload), str(payload.get("body_text") or ""), _message_brief(payload)]).casefold()
    if "регистрационная форма" in name:
        return "регистрационная форма участника курса"
    if Path(name).suffix.lower() == ".pdf" and ("архив" in body or "обучен" in body):
        return "информационное письмо о курсе по архивному делу"
    preview = str(item.get("text_preview") or "").strip()
    if preview and not _looks_like_attachment_noise(preview):
        return _truncate(preview, 120)
    content_type = str(item.get("content_type") or "").lower()
    if content_type.startswith("image/") and any(token in body for token in ["ошибка оплаты", "ошибка", "оплат", "платеж", "платёж"]):
        return "скриншот ошибки оплаты / отклонённого платежа"
    if content_type.startswith("image/"):
        return "изображение без распознанного текста"
    if content_type == "application/pdf" or Path(name).suffix.lower() == ".pdf":
        return "скан документа, текст распознан частично"
    return "содержимое не распознано"


def _render_thread_history(payload: dict[str, Any]) -> list[str]:
    history = case_binding(payload).get("thread_history") or []
    if not isinstance(history, list) or not history:
        return ["нет"]
    out: list[str] = []
    current_message = str(payload.get("message_id") or "").strip()
    for item in history[-3:]:
        if not isinstance(item, dict):
            continue
        direction = _ru_direction(str(item.get("direction", "") or ""))
        sent_at = _short_datetime(str(item.get("sent_at", "") or ""))
        item_subject = str(item.get("subject", "") or "").strip() or "<empty>"
        preview = _thread_preview(item, payload if str(item.get("message_id") or "").strip() == current_message else None)
        subject_part = item_subject if item_subject not in {"<empty>", "Re:"} else "без темы"
        if preview and preview.casefold() not in subject_part.casefold():
            out.append(f"- {_e(direction)} · {_e(sent_at)} · {_e(_truncate(subject_part, 42))} · {_e(_truncate(preview, 92))}")
        else:
            out.append(f"- {_e(direction)} · {_e(sent_at)} · {_e(_truncate(subject_part, 92))}")
    return out or ["нет"]


def _thread_preview(item: dict[str, Any], current_payload: dict[str, Any] | None) -> str:
    if current_payload is not None:
        return _message_brief(current_payload)
    path = str(item.get("parsed_email_path") or "").strip()
    if not path:
        return ""
    try:
        other = load_dossier(path)
    except Exception:
        return ""
    return _message_brief(other)


def _render_understanding(payload: dict[str, Any]) -> list[str]:
    llm = llm_output(payload)
    decision = decision_layer(payload)
    early = early_classification(payload)
    if not llm and not early:
        return ["нет"]
    topic = str(decision.get("classification") or early.get("classification") or llm.get("topic") or "").strip()
    need = str(early.get("operator_summary") or llm.get("customer_need") or "").strip()
    proposal = str(decision.get("decision_reason") or early.get("proposed_action_text") or llm.get("suggested_next_step") or "").strip()
    return [
        f"Тип обращения: {_e(_ru_classification(topic) or _clean_operator_text(str(llm.get('topic', '') or '<empty>')))}",
        f"Что хочет отправитель: {_e(_clean_operator_text(need) or _message_brief(payload))}",
        f"Следующий шаг: {_e(_clean_operator_text(proposal) or _ru_response_mode(response_mode(payload)))}",
    ]


def _render_decision(payload: dict[str, Any]) -> list[str]:
    decision = decision_layer(payload)
    if not decision:
        mode = response_mode(payload)
        reason = str(llm_output(payload).get("response_mode_reason", "") or "").strip()
        route = {}
    else:
        mode = str(decision.get("response_mode_final") or decision.get("response_mode_initial") or "")
        reason = str(decision.get("decision_reason", "") or "").strip()
        route = decision.get("recommended_route") if isinstance(decision.get("recommended_route"), dict) else {}
    lines = [
        f"Режим: {_e(_ru_response_mode(mode))}",
        f"Причина: {_e(_clean_operator_text(reason) or _message_brief(payload))}",
    ]
    route_line = _format_route(route)
    if route_line:
        lines.append(f"Передать: {_e(route_line)}")
    return lines


def _message_brief(payload: dict[str, Any]) -> str:
    llm = llm_output(payload)
    decision = decision_layer(payload)
    early = early_classification(payload)
    mail_subject = subject(payload)
    candidates = [
        str(decision.get("operator_summary", "") or "").strip(),
        str(decision.get("case_summary_short", "") or "").strip(),
        str(early.get("operator_summary", "") or "").strip(),
        str(early.get("case_summary_short", "") or "").strip(),
        str(llm.get("operator_summary", "") or "").strip(),
        str(llm.get("summary", "") or "").strip(),
        str(llm.get("customer_need", "") or "").strip(),
        _body_summary(payload),
        _attachment_summary(payload),
    ]
    for candidate in candidates:
        if not candidate:
            continue
        cleaned = _clean_operator_text(candidate)
        if not cleaned:
            continue
        return _truncate(cleaned, 190)
    if mail_subject:
        return _truncate(f"Письмо по теме: {mail_subject}", 190)
    return "Суть не определена: нужен ручной просмотр письма."


def _clean_operator_text(value: str) -> str:
    text = " ".join(str(value or "").split()).strip()
    if not text:
        return ""
    normalized = text.casefold().replace("ё", "е")
    generic_tokens = {
        "<empty>",
        "нет",
        "входящее обращение",
        "получить ответ или передачу ответственному.",
        "получить ответ или передачу ответственному",
        "кейс требует ручной обработки оператором",
        "модель отметила потребность в ручной обработке.",
        "модель отметила потребность в ручной обработке",
        "fallback meaningful message",
        "meaningful message needs manual review",
    }
    if normalized in generic_tokens:
        return ""
    if normalized.startswith("входящее письмо от") and "без темы" in normalized:
        return ""
    if normalized in {"здравствуйте!", "здравствуйте", "добрый день!", "добрый день", "добрый вечер", "привет"}:
        return ""
    return text


def _body_summary(payload: dict[str, Any]) -> str:
    body = _meaningful_body_excerpt(str(payload.get("body_text") or ""))
    if not body:
        return ""
    return _truncate(body, 180)


def _attachment_summary(payload: dict[str, Any]) -> str:
    items = _attachment_items(payload)
    for item in items:
        preview = str(item.get("text_preview") or "").strip()
        if preview and not _looks_like_attachment_noise(preview):
            return preview
    return ""


def _format_route(route: dict[str, Any]) -> str:
    if not route:
        return ""
    department = str(route.get("department") or "").strip()
    contact_name = str(route.get("contact_name") or "").strip()
    email = str(route.get("email") or "").strip()
    score = str(route.get("score") or "").strip()
    parts = []
    if department:
        parts.append(department)
    if contact_name:
        parts.append(contact_name)
    if email:
        parts.append(email)
    if score:
        parts.append(f"балл {score}")
    return " · ".join(parts)


def _render_knowledge(payload: dict[str, Any]) -> list[str]:
    knowledge = knowledge_retrieval(payload)
    if knowledge.get("status") == "skipped":
        return ["не применялась — письмо не требует клиентской базы знаний по билетам."]
    items = _display_knowledge_items(payload)
    routes = _routing_items(payload)
    if not items and not routes:
        return ["нет"]
    lines = []
    for item in items[:3]:
        title = str(item.get("title", "") or item.get("id", "") or "<empty>")
        item_id = str(item.get("id", "") or "")
        score = str(item.get("score", "") or "")
        suffix = f" / {item_id}" if item_id else ""
        if score:
            suffix += f" / балл {score}"
        lines.append(f"- {_e(_truncate(title, 70) + suffix)}")
    for route in routes[:2]:
        route_line = _format_route(route)
        if route_line:
            lines.append(f"- маршрут: {_e(_truncate(route_line, 90))}")
    return lines


def _render_list(items: Any) -> list[str]:
    if not isinstance(items, list) or not items:
        return ["нет"]
    return [f"- {_e(str(item))}" for item in items[:5] if str(item).strip()] or ["нет"]


def _human_action_type(value: str) -> str:
    mapping = {
        "notify_department_stub": "уведомить отдел",
        "forward_to_chat_stub": "уведомить ответственных",
        "mark_manual_processing": "ручная обработка",
    }
    return mapping.get(str(value or "").strip(), "")


def _ignore_reason(payload: dict[str, Any]) -> str:
    classification = str(early_classification(payload).get("classification") or decision_layer(payload).get("classification") or "")
    mapping = {
        "newsletter_or_promo": "рекламная рассылка",
        "security_or_no_reply_noise": "служебный security/no-reply шум",
        "bounce_or_delivery_noise": "техническое уведомление о доставке",
        "gratitude_or_case_closed": "благодарность / вопрос закрыт",
    }
    return mapping.get(classification, "не требующее ответа письмо")


def _action_request_result_text(payload: dict[str, Any]) -> str:
    text = str(latest_action_suggestion(payload).get("action_text") or "").strip()
    target = _action_target_from_text(text)
    if target:
        return f"письмо передано в {target} в mock-режиме. Реальная маршрутизация пока не подключена."
    return "кейс помечен для ручной обработки. Реальная маршрутизация пока не подключена."


def _action_target_from_text(text: str) -> str:
    normalized = str(text or "").casefold().replace("ё", "е")
    if "платеж" in normalized or "платеж" in normalized or "платёж" in normalized:
        return "ответственный контур по платежам"
    if "практик" in normalized or "hr" in normalized:
        return "отдел практики/HR"
    if "smm" in normalized:
        return "отдел маркетинга/SMM"
    if "партнер" in normalized or "партнерств" in normalized or "партнёр" in normalized or "администрац" in normalized:
        return "отдел партнёрств/маркетинга или администрацию объекта"
    if "документооборот" in normalized or "обучен" in normalized:
        return "ответственным за административное обучение/документооборот"
    if "маркетинг" in normalized:
        return "отдел маркетинга"
    return ""


def _meaningful_body_excerpt(value: str, limit: int = 220) -> str:
    text = str(value or "").replace("\xa0", " ")
    for marker in ["\n\n--", "\n--", "\nКому:", "\nОт:", "-----Original Message-----", "----------------"]:
        if marker in text:
            text = text.split(marker, 1)[0]
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[*_`]+", "", text)
    text = " ".join(text.split()).strip()
    text = re.sub(
        r"^(здравствуйте|добрый день|добрый вечер|доброе утро|привет)[!,. ]+",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()
    if not text:
        return ""
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]
    if not sentences:
        return _truncate(text, limit)
    if len(sentences[0]) < 12 and len(sentences) > 1:
        return _truncate(sentences[1], limit)
    return _truncate(sentences[0], limit)


def _looks_like_attachment_noise(value: str) -> bool:
    text = str(value or "")
    if "PK\x03\x04" in text or "[Content_Types].xml" in text:
        return True
    control_count = sum(1 for char in text if ord(char) < 32 and char not in "\n\r\t")
    return control_count > 3


def _append_card_index(index_path: Path, card_payload: dict[str, Any]) -> None:
    index = read_json(index_path, {"cards": []})
    if not isinstance(index, dict):
        index = {"cards": []}
    cards = index.get("cards")
    if not isinstance(cards, list):
        cards = []
    cards.append(
        {
            "uid": card_payload["uid"],
            "case_id": card_payload["case_id"],
            "thread_id": card_payload["thread_id"],
            "source_dossier_path": card_payload["source_dossier_path"],
            "telegram_message_id": card_payload["telegram_message_id"],
            "telegram_chat_id": card_payload["telegram_chat_id"],
            "callback_data": card_payload["callback_data"],
            "card_text": card_payload["card_text"],
            "card_artifact_path": card_payload["card_artifact_path"],
            "status": card_payload["status"],
            "created_at": card_payload["created_at"],
        }
    )
    index["cards"] = cards
    write_json(index_path, index)


def _next_mock_message_id(state_path: Path) -> int:
    state = read_json(state_path, {"offset": 0})
    if not isinstance(state, dict):
        state = {"offset": 0}
    try:
        current = int(state.get("offset", 0) or 0)
    except Exception:
        current = 0
    current += 1
    state["offset"] = current
    write_json(state_path, state)
    return current


def _ru_direction(value: str) -> str:
    normalized = value.strip().lower()
    if normalized == "outbound":
        return "исходящее"
    if normalized == "inbound":
        return "входящее"
    return normalized or "сообщение"


def _ru_response_mode(value: str) -> str:
    mapping = {
        "answer": "ответить",
        "ask_clarifying_question": "уточнить данные",
        "handoff_to_operator": "передать оператору",
        "no_reply": "не отвечать",
        "no_reply/ignore": "не отвечать / игнорировать",
        "ignore": "игнорировать",
    }
    return mapping.get(str(value or "").strip(), str(value or "").strip() or "не задан")


def _ru_classification(value: str) -> str:
    mapping = {
        "customer_support": "клиентский вопрос",
        "schedule_or_repertoire_question": "вопрос по репертуару/расписанию",
        "business_proposal": "бизнес-предложение",
        "candidate_or_portfolio": "кандидат/портфолио",
        "training_invitation": "приглашение на обучение / административное предложение",
        "gratitude_or_case_closed": "благодарность / вопрос закрыт",
        "service_notification": "служебное уведомление",
        "action_required_notification": "служебное уведомление, требуется действие",
        "newsletter_or_promo": "рекламная рассылка",
        "security_or_no_reply_noise": "no-reply/security уведомление",
        "bounce_or_delivery_noise": "техническое уведомление о доставке",
        "unknown_meaningful": "значимое письмо, нужна ручная оценка",
    }
    return mapping.get(str(value or "").strip(), "")


def _action_label(action: str) -> str:
    mapping = {
        "approve": "утверждено",
        "needs_edit": "на доработку",
        "handoff": "ручная обработка",
        "ignore": "ответ не требуется, кейс закрыт",
        "action_request": "действие зафиксировано в mock-режиме",
    }
    return mapping.get(action, action)


def _short_datetime(value: str) -> str:
    text = value.strip()
    if not text:
        return "дата неизвестна"
    return text.replace("T", " ")[:16]


def _truncate(value: str, limit: int) -> str:
    text = " ".join(value.split())
    if len(text) <= limit:
        return text
    return text[: max(limit - 1, 1)].rstrip() + "…"


def _e(value: str) -> str:
    return html.escape(str(value), quote=False)


def safe_case_dir_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value or "case-unknown")
