from __future__ import annotations

from pathlib import Path

from src.pipeline.operator_flow import (
    build_reply_markup,
    load_dossier,
    persist_operator_card,
    render_operator_card,
    resolve_dossier_input,
    save_dossier,
    read_json,
    write_json,
    timestamp_for_filename,
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
        client: TelegramBotApiClient | None = None,
        operator_chat_id: str | int | None = None,
    ) -> None:
        self.dossier_path = dossier_path
        self.artifacts_dir = artifacts_dir
        self.card_status = card_status
        self.status_notice = status_notice
        self.delivery_mode = delivery_mode
        self.client = client
        self.operator_chat_id = operator_chat_id

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
            client = self.client
            operator_chat_id = self.operator_chat_id
            if self.delivery_mode in {"real", "auto"}:
                if client is None:
                    try:
                        client = TelegramBotApiClient.from_config()
                    except Exception:
                        client = None
                if operator_chat_id is None:
                    try:
                        operator_chat_id = TelegramBotApiClient.operator_delivery_chat_id(self.artifacts_dir)
                    except Exception:
                        operator_chat_id = ""
            should_send_real = self.delivery_mode == "real" or (
                self.delivery_mode == "auto" and client is not None and bool(operator_chat_id)
            )
            if self.delivery_mode == "real" and client is not None and not operator_chat_id:
                telegram_delivery_mode = "waiting_operator_dm"
                telegram_ops.append({
                    "operation": "resolveOperatorDm",
                    "ok": False,
                    "warning": "operator DM is not registered; open private chat with bot and send /start",
                })
            elif should_send_real:
                if client is None:
                    raise RuntimeError("Telegram bot token is not configured")
                if not operator_chat_id:
                    raise RuntimeError(
                        "Telegram operator DM chat id is not configured. Open DM with bot and send /start, "
                        "or set telegram_operator_delivery.operator_dm_chat_id in config.local.yaml."
                    )
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
                telegram_delivery_mode = "telegram_bot_api_dm"
                telegram_ops.extend(_send_attachments(client, operator_chat_id, payload))

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
            if telegram_delivery_mode == "waiting_operator_dm":
                _queue_pending_card(
                    artifacts_dir=self.artifacts_dir,
                    dossier_path=str(dossier_path),
                    card_artifact_path=str(card_payload["card_artifact_path"]),
                    case_id=str(card_payload["case_id"]),
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


def _queue_pending_card(*, artifacts_dir: str, dossier_path: str, card_artifact_path: str, case_id: str) -> None:
    path = Path(artifacts_dir) / "state" / "pending_operator_cards.json"
    data = read_json(path, {"cards": []})
    if not isinstance(data, dict):
        data = {"cards": []}
    cards = data.get("cards")
    if not isinstance(cards, list):
        cards = []
    # Deduplicate by dossier path so the same card is not queued repeatedly.
    for item in cards:
        if isinstance(item, dict) and item.get("dossier_path") == dossier_path and not item.get("sent"):
            item["card_artifact_path"] = card_artifact_path
            item["case_id"] = case_id
            item["updated_at"] = timestamp_for_filename()
            data["cards"] = cards
            write_json(path, data)
            return
    cards.append({
        "dossier_path": dossier_path,
        "card_artifact_path": card_artifact_path,
        "case_id": case_id,
        "queued_at": timestamp_for_filename(),
        "sent": False,
    })
    data["cards"] = cards
    write_json(path, data)


def _send_attachments(client: TelegramBotApiClient, chat_id: str | int, payload: dict) -> list[dict]:
    module = (payload.get("modules") or {}).get("attachment_extraction") or {}
    items = module.get("items") if isinstance(module, dict) else []
    if not isinstance(items, list):
        return []
    operations: list[dict] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        path = str(item.get("saved_path") or "").strip()
        if not path:
            continue
        content_type = str(item.get("content_type") or "").lower()
        description = _attachment_description(payload, item)
        uid_label = _uid_label(payload)
        caption = f"Вложение к {uid_label}: {description}"[:1024]
        if content_type in {"image/png", "image/jpeg", "image/jpg", "image/webp"}:
            result = client.send_photo(chat_id=chat_id, photo_path=path, caption=caption)
        else:
            result = client.send_document(chat_id=chat_id, document_path=path, caption=caption)
        if not result.get("ok"):
            result["warning"] = "attachment delivery failed; card delivery kept"
        operations.append(result)
    return operations


def _uid_label(payload: dict) -> str:
    uid = str((payload.get("metadata") or {}).get("uid") or "").strip()
    return f"raw_email_{uid}" if uid and not uid.startswith("raw_email_") else (uid or "письму")


def _attachment_description(payload: dict, item: dict) -> str:
    name = str(item.get("filename_original") or item.get("filename") or Path(str(item.get("saved_path") or "")).name)
    content_type = str(item.get("content_type") or "").lower()
    extracted = str(item.get("extracted_text_preview") or item.get("text_preview") or item.get("text") or "").strip()
    lower = f"{name} {extracted}".casefold()
    if "билет" in lower or "заказ" in lower or "mooon" in lower or "silverscreen" in lower:
        return f"{name} · электронный билет / билетный документ"
    if "pdf" in content_type or name.casefold().endswith(".pdf"):
        return f"{name} · PDF-документ"
    if "word" in content_type or name.casefold().endswith(".docx"):
        return f"{name} · документ Word"
    if "excel" in content_type or name.casefold().endswith((".xlsx", ".xls")):
        return f"{name} · таблица Excel"
    if content_type.startswith("image/"):
        return f"{name} · изображение"
    return f"{name} · вложенный файл"
