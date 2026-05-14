from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import requests

from src.layers.config.local_yaml_config_store import LocalYamlConfigStore


class TelegramBotApiClient:
    def __init__(
        self,
        *,
        bot_token: str,
        timeout_sec: int = 20,
        base_url: str = "https://api.telegram.org",
    ) -> None:
        self.bot_token = bot_token.strip()
        self.timeout_sec = timeout_sec
        self.base_url = base_url.rstrip("/")

    @classmethod
    def from_config(cls) -> "TelegramBotApiClient | None":
        config = LocalYamlConfigStore().get_section("telegram_operator_delivery")
        token = str(os.getenv("TELEGRAM_BOT_TOKEN") or config.get("bot_token") or "").strip()
        if not token:
            return None
        timeout_sec = int(config.get("timeout_sec") or 20)
        return cls(bot_token=token, timeout_sec=timeout_sec)

    @staticmethod
    def operator_chat_id_from_config() -> str:
        config = LocalYamlConfigStore().get_section("telegram_operator_delivery")
        return str(os.getenv("TELEGRAM_OPERATOR_CHAT_ID") or config.get("operator_chat_id") or "").strip()

    def send_message(
        self,
        *,
        chat_id: str | int,
        text: str,
        reply_markup: dict[str, Any] | None = None,
        reply_to_message_id: int | str | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        if reply_markup is not None:
            payload["reply_markup"] = reply_markup
        if reply_to_message_id is not None:
            payload["reply_parameters"] = {"message_id": reply_to_message_id}
        return self._post("sendMessage", payload)

    def send_photo(self, *, chat_id: str | int, photo_path: str, caption: str = "") -> dict[str, Any]:
        return self._post_file(
            "sendPhoto",
            {"chat_id": chat_id, "caption": caption},
            file_field="photo",
            file_path=photo_path,
        )

    def send_document(self, *, chat_id: str | int, document_path: str, caption: str = "") -> dict[str, Any]:
        return self._post_file(
            "sendDocument",
            {"chat_id": chat_id, "caption": caption},
            file_field="document",
            file_path=document_path,
        )

    def edit_message_text(
        self,
        *,
        chat_id: str | int,
        message_id: int,
        text: str,
        reply_markup: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        if reply_markup is not None:
            payload["reply_markup"] = reply_markup
        return self._post("editMessageText", payload)

    def edit_message_reply_markup(
        self,
        *,
        chat_id: str | int,
        message_id: int,
        reply_markup: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "message_id": message_id,
            "reply_markup": reply_markup or {"inline_keyboard": []},
        }
        return self._post("editMessageReplyMarkup", payload)

    def delete_message(self, *, chat_id: str | int, message_id: int | str) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "message_id": int(message_id),
        }
        return self._post("deleteMessage", payload)

    def answer_callback_query(self, *, callback_query_id: str, text: str = "") -> dict[str, Any]:
        payload: dict[str, Any] = {"callback_query_id": callback_query_id}
        if text:
            payload["text"] = text
        return self._post("answerCallbackQuery", payload)

    def get_updates(self, *, offset: int | None = None, timeout: int = 30) -> dict[str, Any]:
        payload: dict[str, Any] = {"timeout": timeout}
        if offset is not None:
            payload["offset"] = offset
        return self._post("getUpdates", payload)

    def _post(self, method: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}/bot{self.bot_token}/{method}"
        try:
            response = requests.post(url, json=payload, timeout=self.timeout_sec)
            body = response.json() if response.content else {}
        except Exception as exc:
            return {
                "operation": method,
                "ok": False,
                "error": str(exc),
            }

        result: dict[str, Any] = {
            "operation": method,
            "ok": bool(body.get("ok")) and response.ok,
            "status_code": response.status_code,
        }
        if not result["ok"]:
            result["error_code"] = body.get("error_code")
            result["error"] = str(body.get("description") or response.text)
            return result

        api_result = body.get("result")
        if isinstance(api_result, dict):
            result["message_id"] = api_result.get("message_id")
            chat = api_result.get("chat")
            if isinstance(chat, dict):
                result["chat_id"] = chat.get("id")
        elif isinstance(api_result, bool):
            result["result"] = api_result
        else:
            result["result"] = api_result
        return result

    def _post_file(self, method: str, payload: dict[str, Any], *, file_field: str, file_path: str) -> dict[str, Any]:
        path = Path(file_path)
        if not path.exists():
            return {
                "operation": method,
                "ok": False,
                "error": f"file not found: {file_path}",
                "file_path": file_path,
            }
        url = f"{self.base_url}/bot{self.bot_token}/{method}"
        try:
            with path.open("rb") as handle:
                response = requests.post(
                    url,
                    data=payload,
                    files={file_field: (path.name, handle)},
                    timeout=self.timeout_sec,
                )
            body = response.json() if response.content else {}
        except Exception as exc:
            return {
                "operation": method,
                "ok": False,
                "error": str(exc),
                "file_path": file_path,
            }

        result: dict[str, Any] = {
            "operation": method,
            "ok": bool(body.get("ok")) and response.ok,
            "status_code": response.status_code,
            "file_path": file_path,
        }
        if not result["ok"]:
            result["error_code"] = body.get("error_code")
            result["error"] = str(body.get("description") or response.text)
            return result

        api_result = body.get("result")
        if isinstance(api_result, dict):
            result["message_id"] = api_result.get("message_id")
            chat = api_result.get("chat")
            if isinstance(chat, dict):
                result["chat_id"] = chat.get("id")
        return result
