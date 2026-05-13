from __future__ import annotations

from typing import Any

from src.pipeline.draft_builder.module import DraftBuilderModule
from src.pipeline.operator_flow import (
    action_status_notice,
    find_dossier_from_card_index,
    load_dossier,
    parse_callback_data,
    persist_operator_card,
    render_operator_card,
    resolve_dossier_input,
    resolve_uid,
    save_dossier,
    timestamp_for_filename,
    write_json,
)
from src.pipeline.reply_sender.module import ReplySenderModule
from src.shared.contracts.module_contract import ModuleResult
from src.shared.models.entities import OperatorAction
from src.shared.models.pipeline_context import PipelineContext


class OperatorActionsModule:
    name = "operator_actions"

    def __init__(
        self,
        dossier_path: str | None = None,
        artifacts_dir: str = "artifacts",
        action: str = "",
        callback_data: str = "",
        operator_comment: str = "",
        operator_telegram_id: str = "mock_operator",
        operator_username: str = "mock_operator",
    ) -> None:
        self.dossier_path = dossier_path
        self.artifacts_dir = artifacts_dir
        self.action = action
        self.callback_data = callback_data
        self.operator_comment = operator_comment
        self.operator_telegram_id = operator_telegram_id
        self.operator_username = operator_username

    def run(self, context: PipelineContext) -> ModuleResult:
        try:
            action = self._resolve_action()
            if action not in {"approve", "needs_edit", "handoff", "ignore"}:
                raise ValueError(f"Unsupported operator action: {action}")

            dossier_path = self._resolve_dossier_path(context)
            if dossier_path is None:
                return ModuleResult(context=context, status="skipped", notes=["operator_actions skipped: dossier_path missing"])

            payload = load_dossier(dossier_path)
            action_payload = self._build_action_payload(payload, str(dossier_path), action)
            refs = []

            if action == "needs_edit":
                draft_result = DraftBuilderModule(
                    dossier_path=str(dossier_path),
                    operator_comment=self.operator_comment,
                    revision_reason="operator_needs_edit",
                ).run(context)
                refs.extend(draft_result.artifact_refs)
                payload = load_dossier(dossier_path)

            if action == "approve":
                reply_result = ReplySenderModule(
                    dossier_path=str(dossier_path),
                    artifacts_dir=self.artifacts_dir,
                    operator_action=action_payload,
                ).run(context)
                refs.extend(reply_result.artifact_refs)
                action_payload["mock_reply_refs"] = list(reply_result.metrics.get("mock_reply_refs", []))

            payload = load_dossier(dossier_path)
            card_text = render_operator_card(
                payload,
                status_notice=action_status_notice(action, mock_refs=action_payload.get("mock_reply_refs")),
                action=action,
            )
            card_payload = persist_operator_card(
                payload,
                dossier_path=str(dossier_path),
                artifacts_dir=self.artifacts_dir,
                card_text=card_text,
                card_status=f"action_{action}",
                action=action,
            )
            action_payload["updated_card_ref"] = card_payload["card_artifact_path"]
            action_artifact_path = self._write_action_artifact(action_payload)

            self._append_action_to_dossier(payload, action_payload)
            save_dossier(dossier_path, payload)
            refs.extend([action_artifact_path, str(dossier_path), card_payload["card_artifact_path"]])
        except Exception as exc:
            return ModuleResult(context=context, status="error", notes=[f"operator_actions failed: {exc}"])

        context.operator_action = OperatorAction(action=action, note=self.operator_comment)
        context.artifacts.setdefault(self.name, []).extend(refs)
        return ModuleResult(
            context=context,
            status="ok",
            notes=[
                f"operator action processed: {action}",
                "telegram card updated in Russian",
                "real_email_sent=False",
            ],
            artifact_refs=refs,
            metrics=action_payload,
        )

    def _resolve_action(self) -> str:
        if self.callback_data:
            return parse_callback_data(self.callback_data)["action"]
        return self.action.strip()

    def _resolve_dossier_path(self, context: PipelineContext):
        dossier_path = resolve_dossier_input(self.dossier_path, context.artifacts)
        if dossier_path is not None:
            return dossier_path
        if self.callback_data:
            return resolve_dossier_input(find_dossier_from_card_index(self.artifacts_dir, self.callback_data), None)
        return None

    def _build_action_payload(self, payload: dict[str, Any], dossier_path: str, action: str) -> dict[str, Any]:
        callback_data = self.callback_data
        if not callback_data:
            callback_data = f"ma|{action}|{resolve_uid(payload)}|{_case_id(payload)}|{_thread_id(payload)}"
        return {
            "uid": resolve_uid(payload),
            "case_id": _case_id(payload),
            "thread_id": _thread_id(payload),
            "action": action,
            "operator_comment": self.operator_comment.strip(),
            "operator_telegram_id": self.operator_telegram_id,
            "operator_username": self.operator_username,
            "created_at": timestamp_for_filename(),
            "draft_ref": f"{dossier_path}#modules.draft_builder",
            "source_dossier_path": dossier_path,
            "callback_data": callback_data,
            "mock_reply_refs": [],
            "updated_card_ref": "",
            "real_email_sent": False,
        }

    def _write_action_artifact(self, action_payload: dict[str, Any]) -> str:
        target = (
            f"{self.artifacts_dir}/operator_actions/"
            f"{action_payload['case_id']}/action_{action_payload['created_at']}.json"
        )
        return write_json(target, action_payload)

    def _append_action_to_dossier(self, payload: dict[str, Any], action_payload: dict[str, Any]) -> None:
        modules = payload.setdefault("modules", {})
        existing = modules.get(self.name) if isinstance(modules.get(self.name), dict) else {}
        actions = existing.get("actions") if isinstance(existing, dict) else []
        if not isinstance(actions, list):
            actions = []
        actions.append(action_payload)
        modules[self.name] = {
            "status": "ok",
            "latest_action": action_payload,
            "actions": actions,
            "real_email_sent": False,
        }


def _case_id(payload: dict[str, Any]) -> str:
    return str(((payload.get("modules") or {}).get("case_thread_binding") or {}).get("case_id") or "case-unknown")


def _thread_id(payload: dict[str, Any]) -> str:
    return str(((payload.get("modules") or {}).get("case_thread_binding") or {}).get("thread_id") or "thread-unknown")
