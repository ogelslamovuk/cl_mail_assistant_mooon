from __future__ import annotations

from typing import Any

from src.pipeline.draft_builder.module import DraftBuilderModule
from src.pipeline.operator_flow import (
    action_status_notice,
    build_reply_markup,
    latest_action_suggestion,
    find_dossier_from_card_index,
    latest_draft_module,
    latest_draft_text,
    load_dossier,
    needs_edit_waiting_notice,
    parse_callback_data,
    persist_operator_card,
    read_json,
    render_operator_card,
    resolve_uid,
    save_dossier,
    timestamp_for_filename,
    build_action_suggestion_revision,
    write_json,
)
from src.pipeline.reply_sender.module import ReplySenderModule
from src.pipeline.telegram_bot_api import TelegramBotApiClient
from src.shared.common.paths import resolve_project_path
from src.shared.models.pipeline_context import PipelineContext


class OperatorBotHandler:
    def __init__(self, *, artifacts_dir: str = "artifacts", client: TelegramBotApiClient | None = None) -> None:
        self.artifacts_dir = artifacts_dir
        self.client = client or TelegramBotApiClient.from_config()
        if self.client is None:
            raise RuntimeError("Telegram bot token is not configured")

    def handle_callback(
        self,
        *,
        callback_data: str,
        chat_id: int | str,
        message_id: int,
        operator_telegram_id: str = "",
        operator_username: str = "",
        callback_query_id: str = "",
    ) -> dict[str, Any]:
        parsed = parse_callback_data(callback_data)
        action = parsed["action"]
        if action == "needs_edit":
            return self._handle_needs_edit_callback(
                callback_data=callback_data,
                chat_id=chat_id,
                message_id=message_id,
                operator_telegram_id=operator_telegram_id,
                operator_username=operator_username,
                callback_query_id=callback_query_id,
            )
        if action in {"approve", "handoff", "ignore", "action_request"}:
            return self._handle_terminal_callback(
                action=action,
                callback_data=callback_data,
                chat_id=chat_id,
                message_id=message_id,
                operator_telegram_id=operator_telegram_id,
                operator_username=operator_username,
                callback_query_id=callback_query_id,
            )
        raise ValueError(f"Unsupported callback action: {action}")

    def handle_operator_message(
        self,
        *,
        chat_id: int | str,
        text: str,
        message_id: int | None = None,
        reply_to_message_id: int | None = None,
        operator_telegram_id: str = "",
        operator_username: str = "",
    ) -> dict[str, Any]:
        pending = self._get_pending(chat_id)
        if not pending:
            return {"status": "ignored", "reason": "no pending revision request", "bot_api_operations": []}

        dossier_path = str(pending["dossier_path"])
        payload = load_dossier(dossier_path)
        revision_request = {
            "uid": resolve_uid(payload),
            "case_id": pending["case_id"],
            "thread_id": pending["thread_id"],
            "latest_revision": pending.get("latest_revision", 0),
            "operator_comment": text.strip(),
            "operator_telegram_id": operator_telegram_id,
            "operator_username": operator_username,
            "source_callback_data": pending["callback_data"],
            "source_chat_id": pending["chat_id"],
            "source_message_id": pending["message_id"],
            "operator_message_id": message_id,
            "operator_reply_to_message_id": reply_to_message_id,
            "created_at": timestamp_for_filename(),
            "source_dossier_path": dossier_path,
            "status": "created",
        }
        revision_request_path = self._write_revision_request(revision_request)
        self._append_revision_request(payload, revision_request, revision_request_path)
        save_dossier(dossier_path, payload)

        draft_result = DraftBuilderModule(
            dossier_path=dossier_path,
            operator_comment=text,
            revision_reason="operator_needs_edit_comment",
        ).run(PipelineContext(run_id=f"operator-comment-{revision_request['created_at']}"))
        if draft_result.status != "ok":
            raise RuntimeError(f"DraftBuilder failed: {draft_result.notes}")
        payload = load_dossier(dossier_path)
        if not latest_draft_text(payload):
            build_action_suggestion_revision(
                payload,
                dossier_path=dossier_path,
                operator_comment=text,
                revision_reason="operator_needs_edit_comment",
            )
            save_dossier(dossier_path, payload)

        payload = load_dossier(dossier_path)
        card_text = render_operator_card(
            payload,
            status_notice=action_status_notice("needs_edit", payload=payload),
            action="needs_edit",
        )
        update_ops, target_message_id, delivery_mode = self._update_revision_card(
            chat_id=pending["source_chat_id"] if "source_chat_id" in pending else pending["chat_id"],
            message_id=int(pending["message_id"]),
            text=card_text,
            payload=payload,
        )
        cleanup_ops = self._cleanup_revision_messages(
            chat_id=chat_id,
            prompt_message_id=pending.get("prompt_message_id"),
            operator_message_id=message_id,
        )
        ops = update_ops + cleanup_ops
        card_payload = persist_operator_card(
            payload,
            dossier_path=dossier_path,
            artifacts_dir=self.artifacts_dir,
            card_text=card_text,
            card_status="revision_edited" if delivery_mode == "telegram_edit" else "revision_sent_fallback",
            action="needs_edit",
            telegram_message_id=target_message_id,
            telegram_chat_id=chat_id,
            telegram_delivery_mode=delivery_mode,
            telegram_operations=ops,
        )
        save_dossier(dossier_path, payload)

        self._clear_pending(chat_id)
        return {
            "status": "ok",
            "action": "needs_edit_comment",
            "uid": revision_request["uid"],
            "case_id": revision_request["case_id"],
            "thread_id": revision_request["thread_id"],
            "telegram_chat_id": chat_id,
            "telegram_message_id": target_message_id,
            "bot_api_operations": ops,
            "revision_request_path": revision_request_path,
            "card_artifact_path": card_payload["card_artifact_path"],
            "dossier_path": dossier_path,
            "draft_result": draft_result.metrics,
        }

    def _handle_needs_edit_callback(
        self,
        *,
        callback_data: str,
        chat_id: int | str,
        message_id: int,
        operator_telegram_id: str,
        operator_username: str,
        callback_query_id: str,
    ) -> dict[str, Any]:
        dossier_path = find_dossier_from_card_index(self.artifacts_dir, callback_data)
        payload = load_dossier(dossier_path)
        action_payload = self._build_action_payload(
            payload,
            dossier_path,
            "needs_edit",
            callback_data,
            operator_telegram_id,
            operator_username,
        )
        card_text = render_operator_card(payload, status_notice=needs_edit_waiting_notice(), action="")
        ops = self._edit_existing_card(chat_id=chat_id, message_id=message_id, text=card_text)
        if callback_query_id:
            ops.append(
                self.client.answer_callback_query(
                    callback_query_id=callback_query_id,
                    text="Напиши комментарий ответом на сообщение бота.",
                )
            )
        self._assert_required_edits_ok(ops)

        pending_value = {
            "uid": resolve_uid(payload),
            "case_id": self._case_id(payload),
            "thread_id": self._thread_id(payload),
            "dossier_path": dossier_path,
            "callback_data": callback_data,
            "chat_id": chat_id,
            "message_id": message_id,
            "operator_telegram_id": operator_telegram_id,
            "operator_username": operator_username,
            "latest_revision": latest_draft_module(payload).get("latest_revision")
            or ((payload.get("modules") or {}).get("action_suggestion_builder") or {}).get("latest_revision")
            or 0,
            "created_at": timestamp_for_filename(),
        }
        self._set_pending(chat_id, pending_value)

        # Do not send a separate ForceReply prompt here. In this demo group it caused
        # Telegram "inline keyboard expected" errors and left the original card in a
        # broken pending state. The edited card itself is now the prompt: the operator
        # replies to this card or sends the next text message, and the pending state
        # below binds that text to this case.
        card_payload = persist_operator_card(
            payload,
            dossier_path=dossier_path,
            artifacts_dir=self.artifacts_dir,
            card_text=card_text,
            card_status="waiting_operator_comment",
            action="needs_edit",
            telegram_message_id=message_id,
            telegram_chat_id=chat_id,
            telegram_delivery_mode="telegram_bot_api",
            telegram_operations=ops,
        )
        action_payload["updated_card_ref"] = card_payload["card_artifact_path"]
        action_payload["status"] = "waiting_operator_comment"
        action_artifact_path = self._write_action_artifact(action_payload)
        self._append_action(payload, action_payload)
        save_dossier(dossier_path, payload)
        return {
            "status": "ok",
            "action": "needs_edit",
            "uid": resolve_uid(payload),
            "case_id": self._case_id(payload),
            "thread_id": self._thread_id(payload),
            "telegram_chat_id": chat_id,
            "telegram_message_id": message_id,
            "bot_api_operations": ops,
            "operator_action_path": action_artifact_path,
            "card_artifact_path": card_payload["card_artifact_path"],
            "dossier_path": dossier_path,
        }

    def _handle_terminal_callback(
        self,
        *,
        action: str,
        callback_data: str,
        chat_id: int | str,
        message_id: int,
        operator_telegram_id: str,
        operator_username: str,
        callback_query_id: str,
    ) -> dict[str, Any]:
        dossier_path = find_dossier_from_card_index(self.artifacts_dir, callback_data)
        payload = load_dossier(dossier_path)
        action_payload = self._build_action_payload(
            payload,
            dossier_path,
            action,
            callback_data,
            operator_telegram_id,
            operator_username,
        )
        mock_reply_refs: list[str] = []
        if action == "approve":
            if latest_draft_text(payload) and latest_draft_module(payload).get("status") != "skipped":
                reply_result = ReplySenderModule(
                    dossier_path=dossier_path,
                    artifacts_dir=self.artifacts_dir,
                    operator_action=action_payload,
                ).run(PipelineContext(run_id=f"operator-approve-{action_payload['created_at']}"))
                if reply_result.status != "ok":
                    raise RuntimeError(f"ReplySender failed: {reply_result.notes}")
                mock_reply_refs = list(reply_result.metrics.get("mock_reply_refs", []))
                action_payload["mock_reply_refs"] = mock_reply_refs
                payload = load_dossier(dossier_path)
            else:
                action_payload["status"] = "no_draft"
                action_payload["note"] = "approve ignored: no draft available, mock_outbox not created"
        elif action == "action_request":
            suggestion = latest_action_suggestion(payload)
            action_payload["action"] = "action_requested"
            action_payload["action_type"] = str(suggestion.get("action_type") or "mark_manual_processing")
            action_payload["status"] = "stub_recorded"
            action_payload["real_routing"] = False
            action_payload["proposed_action_text"] = str(suggestion.get("action_text") or "")
        elif action == "handoff":
            action_payload["status"] = "manual_processing_marked"
            action_payload["real_routing"] = False
        elif action == "ignore":
            action_payload["status"] = "ignored_no_reply"

        card_text = render_operator_card(
            payload,
            status_notice=action_status_notice(action, mock_refs=mock_reply_refs, payload=payload),
            action=action,
        )
        ops = self._edit_existing_card(chat_id=chat_id, message_id=message_id, text=card_text)
        if callback_query_id:
            ops.append(self.client.answer_callback_query(callback_query_id=callback_query_id, text=_callback_answer_text(action, mock_reply_refs)))
        self._assert_required_edits_ok(ops)

        card_payload = persist_operator_card(
            payload,
            dossier_path=dossier_path,
            artifacts_dir=self.artifacts_dir,
            card_text=card_text,
            card_status=f"action_{action}",
            action=action,
            telegram_message_id=message_id,
            telegram_chat_id=chat_id,
            telegram_delivery_mode="telegram_bot_api",
            telegram_operations=ops,
        )
        action_payload["updated_card_ref"] = card_payload["card_artifact_path"]
        action_artifact_path = self._write_action_artifact(action_payload)
        self._append_action(payload, action_payload)
        save_dossier(dossier_path, payload)
        return {
            "status": "ok",
            "action": action,
            "uid": resolve_uid(payload),
            "case_id": self._case_id(payload),
            "thread_id": self._thread_id(payload),
            "telegram_chat_id": chat_id,
            "telegram_message_id": message_id,
            "bot_api_operations": ops,
            "operator_action_path": action_artifact_path,
            "card_artifact_path": card_payload["card_artifact_path"],
            "mock_reply_refs": mock_reply_refs,
            "dossier_path": dossier_path,
            "real_email_sent": False,
            "real_routing": False,
        }

    def _edit_existing_card(self, *, chat_id: int | str, message_id: int, text: str) -> list[dict[str, Any]]:
        transient_markup = {
            "inline_keyboard": [[{"text": "Обработано", "callback_data": "ma|noop|done"}]]
        }
        edit_text = self.client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=transient_markup,
        )
        edit_markup = self.client.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup={"inline_keyboard": []},
        )
        return [edit_text, edit_markup]

    def _update_revision_card(
        self,
        *,
        chat_id: int | str,
        message_id: int,
        text: str,
        payload: dict[str, Any],
    ) -> tuple[list[dict[str, Any]], int, str]:
        edit_result = self.client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=build_reply_markup(payload),
        )
        edit_ops = [edit_result]
        if edit_result.get("ok"):
            return edit_ops, message_id, "telegram_edit"

        stale_text = "Эта карточка устарела: актуальная версия отправлена ниже."
        stale_ops = self._edit_existing_card(chat_id=chat_id, message_id=message_id, text=stale_text)
        send_result = self.client.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=build_reply_markup(payload),
        )
        if not send_result.get("ok"):
            errors = "; ".join(
                f"{item.get('operation')}: {item.get('error')}"
                for item in [*edit_ops, *stale_ops, send_result]
                if not item.get("ok")
            )
            raise RuntimeError(f"Telegram revision card update failed. {errors}")
        return [*edit_ops, *stale_ops, send_result], int(send_result.get("message_id") or message_id), "telegram_send_fallback"

    def _cleanup_revision_messages(
        self,
        *,
        chat_id: int | str,
        prompt_message_id: Any,
        operator_message_id: int | None,
    ) -> list[dict[str, Any]]:
        ops: list[dict[str, Any]] = []
        for candidate in [prompt_message_id, operator_message_id]:
            if candidate in {None, ""}:
                continue
            try:
                result = self.client.delete_message(chat_id=chat_id, message_id=int(candidate))
            except Exception as exc:
                result = {"operation": "deleteMessage", "ok": False, "error": str(exc), "message_id": candidate}
            if not result.get("ok"):
                result["warning"] = "best-effort cleanup failed; revision card was updated"
            ops.append(result)
        return ops

    @staticmethod
    def _assert_required_edits_ok(ops: list[dict[str, Any]]) -> None:
        required = {"editMessageText", "editMessageReplyMarkup"}
        seen = {str(item.get("operation")) for item in ops if item.get("ok")}
        missing = sorted(required - seen)
        if missing:
            errors = "; ".join(f"{item.get('operation')}: {item.get('error')}" for item in ops if not item.get("ok"))
            raise RuntimeError(f"Telegram edit operations failed or missing: {', '.join(missing)}. {errors}")

    def _build_action_payload(
        self,
        payload: dict[str, Any],
        dossier_path: str,
        action: str,
        callback_data: str,
        operator_telegram_id: str,
        operator_username: str,
    ) -> dict[str, Any]:
        return {
            "uid": resolve_uid(payload),
            "case_id": self._case_id(payload),
            "thread_id": self._thread_id(payload),
            "action": action,
            "operator_comment": "",
            "operator_telegram_id": operator_telegram_id,
            "operator_username": operator_username,
            "created_at": timestamp_for_filename(),
            "draft_ref": f"{dossier_path}#modules.draft_builder",
            "source_dossier_path": dossier_path,
            "callback_data": callback_data,
            "mock_reply_refs": [],
            "updated_card_ref": "",
            "real_email_sent": False,
        }

    def _write_action_artifact(self, action_payload: dict[str, Any]) -> str:
        return write_json(
            f"{self.artifacts_dir}/operator_actions/{action_payload['case_id']}/"
            f"action_{action_payload['created_at']}.json",
            action_payload,
        )

    def _write_revision_request(self, revision_request: dict[str, Any]) -> str:
        return write_json(
            f"{self.artifacts_dir}/revision_requests/{revision_request['case_id']}/"
            f"revision_request_{revision_request['created_at']}.json",
            revision_request,
        )

    @staticmethod
    def _append_action(payload: dict[str, Any], action_payload: dict[str, Any]) -> None:
        modules = payload.setdefault("modules", {})
        existing = modules.get("operator_actions") if isinstance(modules.get("operator_actions"), dict) else {}
        actions = existing.get("actions") if isinstance(existing, dict) else []
        if not isinstance(actions, list):
            actions = []
        actions.append(action_payload)
        modules["operator_actions"] = {
            "status": "ok",
            "latest_action": action_payload,
            "actions": actions,
            "real_email_sent": False,
        }

    @staticmethod
    def _append_revision_request(payload: dict[str, Any], revision_request: dict[str, Any], path: str) -> None:
        modules = payload.setdefault("modules", {})
        existing = modules.get("revision_requests") if isinstance(modules.get("revision_requests"), dict) else {}
        requests = existing.get("requests") if isinstance(existing, dict) else []
        if not isinstance(requests, list):
            requests = []
        item = dict(revision_request)
        item["artifact_path"] = path
        requests.append(item)
        modules["revision_requests"] = {
            "status": "ok",
            "latest_request": item,
            "requests": requests,
        }

    def _pending_path(self):
        return resolve_project_path(self.artifacts_dir) / "state" / "operator_bot_pending.json"

    def _get_pending(self, chat_id: int | str) -> dict[str, Any] | None:
        pending = read_json(self._pending_path(), {"pending": {}})
        entries = pending.get("pending") if isinstance(pending, dict) else {}
        if not isinstance(entries, dict):
            return None
        value = entries.get(str(chat_id))
        return value if isinstance(value, dict) else None

    def _set_pending(self, chat_id: int | str, value: dict[str, Any]) -> None:
        path = self._pending_path()
        pending = read_json(path, {"pending": {}})
        if not isinstance(pending, dict):
            pending = {"pending": {}}
        entries = pending.get("pending")
        if not isinstance(entries, dict):
            entries = {}
        entries[str(chat_id)] = value
        pending["pending"] = entries
        write_json(path, pending)

    def _clear_pending(self, chat_id: int | str) -> None:
        path = self._pending_path()
        pending = read_json(path, {"pending": {}})
        if not isinstance(pending, dict):
            return
        entries = pending.get("pending")
        if not isinstance(entries, dict):
            return
        entries.pop(str(chat_id), None)
        pending["pending"] = entries
        write_json(path, pending)

    @staticmethod
    def _case_id(payload: dict[str, Any]) -> str:
        return str(((payload.get("modules") or {}).get("case_thread_binding") or {}).get("case_id") or "case-unknown")

    @staticmethod
    def _thread_id(payload: dict[str, Any]) -> str:
        return str(((payload.get("modules") or {}).get("case_thread_binding") or {}).get("thread_id") or "thread-unknown")


def _callback_answer_text(action: str, mock_reply_refs: list[str]) -> str:
    if action == "approve":
        return "Mock-ответ создан." if mock_reply_refs else "Черновик отсутствует, mock-ответ не создан."
    if action == "handoff":
        return "Кейс помечен для ручной обработки."
    if action == "ignore":
        return "Кейс помечен как не требующий ответа."
    if action == "action_request":
        return "Действие зафиксировано. Реальная маршрутизация пока не подключена."
    return "Действие обработано."
