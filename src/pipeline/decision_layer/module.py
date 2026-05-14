from __future__ import annotations

import re
from typing import Any

from src.pipeline.early_classification import early_classification
from src.pipeline.operator_flow import load_dossier, resolve_uid, save_dossier
from src.shared.common.paths import resolve_project_path
from src.shared.contracts.module_contract import ModuleResult
from src.shared.models.pipeline_context import PipelineContext


class DecisionLayerModule:
    name = "decision_layer"

    def __init__(self, dossier_path: str) -> None:
        self.dossier_path = dossier_path

    def run(self, context: PipelineContext) -> ModuleResult:
        try:
            dossier_path = resolve_project_path(self.dossier_path)
            payload = load_dossier(dossier_path)
            decision = _decide(payload)
            payload.setdefault("modules", {})[self.name] = decision
            save_dossier(dossier_path, payload)
        except Exception as exc:
            return ModuleResult(context=context, status="error", notes=[f"decision_layer failed: {exc}"])

        context.artifacts.setdefault(self.name, []).append(str(dossier_path))
        return ModuleResult(
            context=context,
            status="ok",
            notes=[
                f"decision_layer processed uid={decision['uid']}",
                f"response_mode_final={decision['response_mode_final']}",
            ],
            artifact_refs=[str(dossier_path)],
            metrics=decision,
        )


def _decide(payload: dict[str, Any]) -> dict[str, Any]:
    modules = payload.get("modules") or {}
    llm = (modules.get("llm_understanding") or {}).get("structured_output") or {}
    enrichment = (modules.get("identity_context_enrichment") or {}).get("result") or {}
    knowledge = modules.get("knowledge_retrieval") or {}
    classification = early_classification(payload)
    initial = str(classification.get("response_mode_hint") or llm.get("response_mode") or "ask_clarifying_question").strip()
    initial = initial or "ask_clarifying_question"
    final = initial
    missing_data: list[str] = []
    risks: list[str] = []
    reason = str(llm.get("response_mode_reason") or "").strip() or "Решение основано на structured understanding."

    body = " ".join(
        str(value or "")
        for value in [
            (payload.get("headers") or {}).get("subject"),
            payload.get("body_text"),
            llm.get("summary"),
            llm.get("topic"),
            llm.get("customer_need"),
        ]
    ).casefold()
    ticket_related = any(token in body for token in ["билет", "ticket", "оплат", "заказ", "квитанц"])
    payment_error = any(token in body for token in ["ошибка оплаты", "ошибка платеж", "ошибка платёж"]) or (
        any(token in body for token in ["оплат", "платеж", "платёж"]) and any(token in body for token in ["ошибка", "выбивает", "отклон"])
    )
    giftcard_related = any(token in body for token in ["подароч", "сертификат", "карта", "карту", "карты"]) and any(
        token in body for token in ["остаток", "актив", "не активна", "баланс", "номинал", "проверь"]
    )
    resolved_match = enrichment.get("resolved_match")

    matched_items = knowledge.get("matched_items") if isinstance(knowledge, dict) else []
    knowledge_ids = [
        str(item.get("id") or "")
        for item in matched_items or []
        if isinstance(item, dict) and str(item.get("id") or "").strip()
    ]

    routing_matches = knowledge.get("routing_matches") if isinstance(knowledge, dict) else []
    recommended_route = _first_route(routing_matches)
    routing_ids = [
        str(item.get("id") or "")
        for item in routing_matches or []
        if isinstance(item, dict) and str(item.get("id") or "").strip()
    ]

    early_class = str(classification.get("classification") or "")
    if early_class in {"newsletter_or_promo", "security_or_no_reply_noise", "bounce_or_delivery_noise", "gratitude_or_case_closed"}:
        final = "no_reply"
        reason = _early_reason(classification, fallback="Письмо не требует клиентского ответа.")
    elif early_class == "action_required_notification":
        final = "handoff_to_operator"
        reason = str(classification.get("operator_summary") or "").strip() or "Служебное уведомление требует ручного действия."
        risks.append("Реальная маршрутизация пока не подключена; доступна только фиксация действия в artifacts.")
    elif early_class in {"business_proposal", "candidate_or_portfolio", "training_invitation"}:
        final = "handoff_to_operator"
        reason = str(classification.get("proposed_action_text") or "").strip() or _early_reason(
            classification,
            fallback="Письмо требует ручной обработки ответственными.",
        )
    elif early_class == "schedule_or_repertoire_question":
        final = "handoff_to_operator"
        reason = "Вопрос касается репертуара/расписания; live schedule connector пока не подключён."
        risks.append("Нельзя отвечать фактом о показах без проверки актуального расписания.")
    elif payload.get("is_bounce") or payload.get("is_auto_reply"):
        final = "no_reply"
        reason = "Письмо похоже на автоматическое техническое уведомление."
    elif initial in {"ignore", "no_reply"}:
        final = initial
    elif bool(llm.get("needs_human")) or str(llm.get("risk_level") or "") == "high":
        final = "handoff_to_operator"
        reason = str(llm.get("response_mode_reason") or "").strip() or "Нужна ручная проверка перед ответом."
        risks.append("Требуется ручная проверка перед ответом.")
    elif giftcard_related:
        final = "ask_clarifying_question"
        reason = "Гость просит проверить подарочную карту; для проверки нужен номер/код карты или скрин ошибки."
        missing_data.extend(_missing_giftcard_data(payload))
    elif ticket_related and resolved_match:
        final = "answer"
        reason = "Билет/заказ найден в проверке билетов; уточнять email, телефон или номер заказа не нужно."
    elif ticket_related and not resolved_match:
        final = "ask_clarifying_question"
        reason = "Письмо связано с билетом/оплатой, но подтвержденный заказ не найден в enrichment."
        missing_data.extend(_missing_ticket_data(payload, payment_error=payment_error))
    elif recommended_route:
        final = "handoff_to_operator"
        reason = _route_reason(recommended_route)
    elif initial == "answer":
        final = "answer"
        reason = reason or "Достаточно фактов для безопасного ответа."

    if not knowledge_ids and final == "answer":
        final = "handoff_to_operator"
        reason = "Нет подходящих записей базы знаний для безопасного автоматического ответа."
        risks.append("Ответ без базы знаний может быть неполным.")

    return {
        "uid": resolve_uid(payload),
        "status": "ok",
        "error": "",
        "response_mode_initial": initial,
        "response_mode_final": final,
        "decision_reason": reason,
        "missing_data": missing_data,
        "risks": risks,
        "knowledge_item_ids": knowledge_ids,
        "routing_item_ids": routing_ids,
        "recommended_route": recommended_route,
        "operator_summary": str(classification.get("operator_summary") or llm.get("summary") or "").strip(),
        "case_summary_short": str(classification.get("case_summary_short") or classification.get("operator_summary") or "").strip(),
        "classification": early_class,
        "should_build_customer_draft": bool(classification.get("should_build_customer_draft", True)),
        "proposed_action_type": str(classification.get("proposed_action_type") or ""),
        "proposed_action_text": str(classification.get("proposed_action_text") or ""),
        "action_stub_allowed": bool(classification.get("action_stub_allowed")),
        "real_email_sent": False,
    }


def _early_reason(classification: dict[str, Any], *, fallback: str) -> str:
    summary = str(classification.get("operator_summary") or "").strip()
    reason = str(classification.get("classification_reason") or "").strip()
    if summary:
        return summary
    if reason:
        return reason
    return fallback


def _missing_giftcard_data(payload: dict[str, Any]) -> list[str]:
    text = " ".join(
        str(value or "")
        for value in [
            ((payload.get("headers") or {}).get("sender")),
            payload.get("body_text"),
        ]
    )
    has_long_number = bool(re.search(r"\b\d{6,}\b", text))
    if has_long_number:
        return ["Скрин ошибки «карта не активна», если он есть."]
    return ["Номер или код подарочной карты для проверки остатка и статуса активации."]


def _missing_ticket_data(payload: dict[str, Any], *, payment_error: bool) -> list[str]:
    text = " ".join(
        str(value or "")
        for value in [
            ((payload.get("headers") or {}).get("sender")),
            payload.get("body_text"),
        ]
    )
    has_email = "@" in text
    has_phone = bool(re.search(r"\+?\d[\d\s().-]{7,}\d", text))
    has_attachment = bool(((payload.get("modules") or {}).get("attachment_extraction") or {}).get("items"))
    if payment_error:
        missing = []
        if not has_attachment:
            missing.append("Скриншот ошибки оплаты.")
        missing.append("Время попытки оплаты и последние 4 цифры карты/банк, если это потребуется для проверки.")
        return missing
    missing = []
    if not has_email and not has_phone:
        missing.append("Email или телефон, указанный при покупке.")
    missing.append("Номер заказа или билета, если он есть у гостя.")
    return missing


def _first_route(routes: Any) -> dict[str, Any]:
    if not isinstance(routes, list):
        return {}
    for item in routes:
        if not isinstance(item, dict):
            continue
        email = str(item.get("email") or "").strip()
        department = str(item.get("department") or "").strip()
        if email or department:
            return item
    return {}


def _route_reason(route: dict[str, Any]) -> str:
    department = str(route.get("department") or "ответственный отдел").strip()
    contact_name = str(route.get("contact_name") or "").strip()
    email = str(route.get("email") or "").strip()
    recipient = " · ".join(part for part in [contact_name, email] if part)
    if recipient:
        return f"Письмо относится к направлению «{department}». Рекомендуется передать на {recipient}."
    return f"Письмо относится к направлению «{department}». Рекомендуется передать ответственным."
