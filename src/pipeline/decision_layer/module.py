from __future__ import annotations

from typing import Any

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
    initial = str(llm.get("response_mode") or "ask_clarifying_question").strip() or "ask_clarifying_question"
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
    resolved_match = enrichment.get("resolved_match")

    if payload.get("is_bounce") or payload.get("is_auto_reply"):
        final = "no_reply"
        reason = "Письмо похоже на автоматическое техническое уведомление."
    elif initial in {"ignore", "no_reply"}:
        final = initial
    elif bool(llm.get("needs_human")) or str(llm.get("risk_level") or "") == "high":
        final = "handoff_to_operator"
        reason = "Модель отметила потребность в ручной обработке."
        risks.append("Требуется ручная проверка перед ответом.")
    elif ticket_related and not resolved_match:
        final = "ask_clarifying_question"
        reason = "Письмо связано с билетом/оплатой, но подтвержденный заказ не найден в enrichment."
        missing_data.append("Номер заказа, телефон или email, указанный при покупке.")
    elif initial == "answer":
        final = "answer"
        reason = reason or "Достаточно фактов для безопасного ответа."

    matched_items = knowledge.get("matched_items") if isinstance(knowledge, dict) else []
    knowledge_ids = [
        str(item.get("id") or "")
        for item in matched_items or []
        if isinstance(item, dict) and str(item.get("id") or "").strip()
    ]

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
        "real_email_sent": False,
    }
