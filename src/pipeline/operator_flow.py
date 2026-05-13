from __future__ import annotations

import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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
            "revision": int(draft.get("latest_revision") or 1),
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


def build_draft_revision(
    payload: dict[str, Any],
    *,
    dossier_path: str,
    operator_comment: str = "",
    revision_reason: str = "initial",
) -> dict[str, Any]:
    existing = draft_revisions(payload)
    revision = len(existing) + 1
    mode = response_mode(payload)
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
            f"От: {_e(sender(payload) or '<empty>')}",
            f"Тема: {_e(subject(payload) or '<empty>')}",
            "",
            "<b>Кейс</b>",
            f"Case ID: {_e(case_id(payload))} · Thread ID: {_e(thread_id(payload))}",
        ]
    )

    lines.extend(["", "<b>Обогащение</b>", _e(_compact_enrichment(payload))])
    lines.extend(["", "<b>История</b>"])
    lines.extend(_render_thread_history(payload))
    lines.extend(["", "<b>Понимание</b>"])
    lines.extend(_render_understanding(payload))
    lines.extend(["", "<b>Решение системы</b>"])
    lines.extend(_render_decision(payload))
    lines.extend(["", "<b>База знаний</b>"])
    lines.extend(_render_knowledge(payload))
    lines.extend(["", "<b>Что не хватает</b>"])
    lines.extend(_render_list(decision_layer(payload).get("missing_data") or []))
    lines.extend(["", "<b>Риски</b>"])
    lines.extend(_render_list(decision_layer(payload).get("risks") or []))

    draft_text = latest_draft_text(payload)
    draft = latest_draft_module(payload)
    latest_revision = draft.get("latest_revision") or (len(draft_revisions(payload)) or 1)
    lines.extend(["", f"<b>Черновик v{_e(str(latest_revision))}</b>"])
    lines.append(_e(draft_text or "нет"))

    if action:
        lines.extend(["", f"<b>Последнее действие</b>", _e(_action_label(action))])

    return "\n".join(lines)


def persist_operator_card(
    payload: dict[str, Any],
    *,
    dossier_path: str,
    artifacts_dir: str,
    card_text: str,
    card_status: str,
    action: str = "",
) -> dict[str, Any]:
    base_dir = resolve_project_path(artifacts_dir)
    state_dir = base_dir / "state"
    state_dir.mkdir(parents=True, exist_ok=True)
    message_id = _next_mock_message_id(state_dir / "operator_bot_state.json")
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
        "telegram_chat_id": TELEGRAM_CHAT_ID_MOCK,
        "telegram_delivery_mode": "mock_artifact_only",
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
    uid = resolve_uid(payload)
    cid = case_id(payload)
    tid = thread_id(payload)
    labels = {
        "approve": "✅ Утвердить",
        "needs_edit": "✏️ На доработку (LLM)",
        "handoff": "👤 Оператору",
        "ignore": "🗑️ Игнорировать",
    }
    return [
        {
            "action": action,
            "label": label,
            "callback_data": f"{CALLBACK_PREFIX}|{action}|{uid}|{cid}|{tid}",
        }
        for action, label in labels.items()
    ]


def parse_callback_data(callback_data: str) -> dict[str, str]:
    parts = str(callback_data or "").split("|")
    if len(parts) != 5 or parts[0] != CALLBACK_PREFIX:
        raise ValueError("Invalid callback_data")
    return {
        "action": parts[1],
        "uid": parts[2],
        "case_id": parts[3],
        "thread_id": parts[4],
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
        if str(card.get("uid", "")) != parsed["uid"]:
            continue
        if str(card.get("case_id", "")) != parsed["case_id"]:
            continue
        dossier = str(card.get("source_dossier_path") or card.get("dossier_path") or "").strip()
        if dossier:
            return dossier
    raise FileNotFoundError("No card index entry found for callback_data")


def action_status_notice(action: str, *, mock_refs: list[str] | None = None) -> str:
    if action == "approve":
        return "✅ Утверждено оператором. Черновик сохранен в mock_outbox. Реальная отправка отключена."
    if action == "needs_edit":
        return "✏️ Черновик доработан по комментарию оператора. Создана новая ревизия."
    if action == "handoff":
        return "👤 Кейс передан оператору для ручной обработки. Реальная отправка отключена."
    if action == "ignore":
        return "🗑️ Кейс помечен как не требующий ответа. Реальная отправка отключена."
    return "Действие оператора обработано. Реальная отправка отключена."


def _build_draft_text(payload: dict[str, Any], *, mode: str, operator_comment: str, prior_text: str) -> str:
    comment = operator_comment.strip()
    if comment and prior_text:
        return _revise_draft(prior_text, comment)

    decision = decision_layer(payload)
    llm = llm_output(payload)
    missing = [str(item).strip() for item in decision.get("missing_data") or [] if str(item).strip()]
    knowledge_lines = _knowledge_template_lines(payload)
    need = str(llm.get("customer_need", "") or "обращение").strip()

    if mode in {"no_reply", "ignore"}:
        reason = str(decision.get("decision_reason") or llm.get("response_mode_reason") or "Ответ не требуется").strip()
        return reason

    if mode == "handoff_to_operator":
        return "Кейс требует ручной обработки оператором. Клиенту пока не отправляется автоматический ответ."

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


def _revise_draft(prior_text: str, operator_comment: str) -> str:
    text = prior_text.strip()
    comment = " ".join(operator_comment.split())
    addition = f"Дополнительно: {comment}"
    if addition in text:
        return text
    if "С уважением, команда mooon." in text:
        return text.replace("С уважением, команда mooon.", f"{addition}\nС уважением, команда mooon.")
    return f"{text}\n{addition}"


def _knowledge_template_lines(payload: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for item in _knowledge_items(payload)[:3]:
        hint = str(item.get("template_hint") or item.get("operator_instruction") or item.get("content") or "").strip()
        if hint:
            lines.append(hint)
    return lines


def _knowledge_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    value = knowledge_retrieval(payload).get("matched_items") or []
    return [item for item in value if isinstance(item, dict)]


def _compact_enrichment(payload: dict[str, Any]) -> str:
    result = enrichment_result(payload)
    debug = enrichment_module(payload).get("debug") or {}
    providers = debug.get("providers") if isinstance(debug, dict) else {}
    ticket_provider = (providers or {}).get("ticket_db") or {}
    resolved = result.get("resolved_match") or {}
    candidates = ticket_provider.get("candidates") or []
    lookup_email = str(result.get("selected_lookup_email") or "").strip() or "не выбран"
    status = str(result.get("ticket_db_status") or "").strip() or "нет данных"
    confidence = str(result.get("confidence") or "").strip() or "нет"
    if isinstance(resolved, dict) and resolved:
        ticket_line = _compact_ticket(resolved)
    else:
        count = result.get("candidates_count")
        if count in (None, ""):
            count = len(candidates) if isinstance(candidates, list) else 0
        ticket_line = f"Билет: не найден · кандидатов: {count}"
    return f"Поиск: {lookup_email} · база билетов: {status} · уверенность: {confidence}\n{ticket_line}"


def _compact_ticket(ticket: dict[str, Any]) -> str:
    parts = [
        f"Билет #{ticket.get('ticket')}" if ticket.get("ticket") else "Билет найден",
        f"заказ {ticket.get('idTrading')}" if ticket.get("idTrading") else "",
        str(ticket.get("event") or ""),
        " ".join(str(ticket.get(key) or "") for key in ("dateShow", "timeShow")).strip(),
        str(ticket.get("theater") or ""),
    ]
    return " · ".join(part for part in parts if part)


def _render_thread_history(payload: dict[str, Any]) -> list[str]:
    history = case_binding(payload).get("thread_history") or []
    if not isinstance(history, list) or not history:
        return ["нет"]
    out: list[str] = []
    for item in history[-3:]:
        if not isinstance(item, dict):
            continue
        direction = _ru_direction(str(item.get("direction", "") or ""))
        sent_at = _short_datetime(str(item.get("sent_at", "") or ""))
        item_subject = str(item.get("subject", "") or "").strip() or "<empty>"
        out.append(f"- {_e(direction)} · {_e(sent_at)} · {_e(_truncate(item_subject, 72))}")
    return out or ["нет"]


def _render_understanding(payload: dict[str, Any]) -> list[str]:
    llm = llm_output(payload)
    if not llm:
        return ["нет"]
    return [
        f"Тема: {_e(str(llm.get('topic', '') or '<empty>'))}",
        f"Потребность: {_e(str(llm.get('customer_need', '') or '<empty>'))}",
        f"Режим: {_e(_ru_response_mode(str(llm.get('response_mode', '') or '')))}",
    ]


def _render_decision(payload: dict[str, Any]) -> list[str]:
    decision = decision_layer(payload)
    if not decision:
        mode = response_mode(payload)
        reason = str(llm_output(payload).get("response_mode_reason", "") or "").strip()
    else:
        mode = str(decision.get("response_mode_final") or decision.get("response_mode_initial") or "")
        reason = str(decision.get("decision_reason", "") or "").strip()
    return [
        f"Режим: {_e(_ru_response_mode(mode))}",
        f"Причина: {_e(reason or 'нет')}",
    ]


def _render_knowledge(payload: dict[str, Any]) -> list[str]:
    items = _knowledge_items(payload)
    if not items:
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
    return lines


def _render_list(items: Any) -> list[str]:
    if not isinstance(items, list) or not items:
        return ["нет"]
    return [f"- {_e(str(item))}" for item in items[:5] if str(item).strip()] or ["нет"]


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
        "ignore": "игнорировать",
    }
    return mapping.get(str(value or "").strip(), str(value or "").strip() or "не задан")


def _action_label(action: str) -> str:
    mapping = {
        "approve": "утверждено",
        "needs_edit": "на доработку",
        "handoff": "передано оператору",
        "ignore": "игнорировано",
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
