from __future__ import annotations

from src.pipeline.operator_flow import (
    build_reply_markup,
    load_dossier,
    persist_operator_card,
    render_operator_card,
    resolve_dossier_input,
    save_dossier,
)
from src.pipeline.telegram_bot_api import TelegramBotApiClient
from src.shared.contracts.module_contract import ModuleResult
from src.shared.models.entities import OperatorCard
from src.shared.models.pipeline_context import PipelineContext


class TelegramOperatorDeliveryModule:
    name = "telegram_operator_delivery"

    def __init__(
        self,
        dossier_path: str | None = None,
        artifacts_dir: str = "artifacts",
        card_status: str = "mock_sent",
        status_notice: str = "",
        delivery_mode: str = "auto",
    ) -> None:
        self.dossier_path = dossier_path
        self.artifacts_dir = artifacts_dir
        self.card_status = card_status
        self.status_notice = status_notice
        self.delivery_mode = delivery_mode

    def run(self, context: PipelineContext) -> ModuleResult:
        dossier_path = resolve_dossier_input(self.dossier_path, context.artifacts)
        if dossier_path is None:
            return ModuleResult(
                context=context,
                status="skipped",
                notes=["telegram_operator_delivery skipped: dossier_path missing"],
            )

        try:
            payload = load_dossier(dossier_path)
            card_text = render_operator_card(payload, status_notice=self.status_notice)
            telegram_ops = []
            telegram_message_id = None
            telegram_chat_id = None
            telegram_delivery_mode = "artifact_only"
            client = TelegramBotApiClient.from_config()
            operator_chat_id = TelegramBotApiClient.operator_chat_id_from_config()
            should_send_real = self.delivery_mode == "real" or (
                self.delivery_mode == "auto" and client is not None and bool(operator_chat_id)
            )
            if should_send_real:
                if client is None:
                    raise RuntimeError("Telegram bot token is not configured")
                if not operator_chat_id:
                    raise RuntimeError("Telegram operator chat id is not configured")
                send_result = client.send_message(
                    chat_id=operator_chat_id,
                    text=card_text,
                    reply_markup=build_reply_markup(payload),
                )
                telegram_ops.append(send_result)
                if not send_result.get("ok"):
                    raise RuntimeError(f"Telegram sendMessage failed: {send_result.get('error')}")
                telegram_message_id = send_result.get("message_id")
                telegram_chat_id = send_result.get("chat_id") or operator_chat_id
                telegram_delivery_mode = "telegram_bot_api"

            card_payload = persist_operator_card(
                payload,
                dossier_path=str(dossier_path),
                artifacts_dir=self.artifacts_dir,
                card_text=card_text,
                card_status=self.card_status,
                telegram_message_id=telegram_message_id,
                telegram_chat_id=telegram_chat_id,
                telegram_delivery_mode=telegram_delivery_mode,
                telegram_operations=telegram_ops,
            )
            save_dossier(dossier_path, payload)
        except Exception as exc:
            return ModuleResult(context=context, status="error", notes=[f"telegram_operator_delivery failed: {exc}"])

        card_path = str(card_payload["card_artifact_path"])
        context.operator_card = OperatorCard(case_id=str(card_payload["case_id"]), summary=card_text)
        context.artifacts.setdefault(self.name, []).extend([str(dossier_path), card_path])
        notes = [
            f"telegram_operator_delivery wrote card case_id={card_payload['case_id']}",
            f"telegram_message_id={card_payload['telegram_message_id']}",
            f"telegram_delivery_mode={card_payload['telegram_delivery_mode']}",
        ]
        return ModuleResult(
            context=context,
            status="ok",
            notes=notes,
            artifact_refs=[str(dossier_path), card_path],
            metrics=card_payload,
        )
