from __future__ import annotations

from typing import Any

from src.pipeline.operator_flow import (
    case_id,
    latest_draft_module,
    latest_draft_text,
    load_dossier,
    resolve_dossier_input,
    resolve_uid,
    safe_case_dir_name,
    save_dossier,
    sender,
    subject,
    thread_id,
    timestamp_for_filename,
    write_json,
)
from src.shared.common.paths import resolve_project_path
from src.shared.contracts.module_contract import ModuleResult
from src.shared.models.pipeline_context import PipelineContext


class ReplySenderModule:
    name = "reply_sender"

    def __init__(
        self,
        dossier_path: str | None = None,
        artifacts_dir: str = "artifacts",
        operator_action: dict[str, Any] | None = None,
    ) -> None:
        self.dossier_path = dossier_path
        self.artifacts_dir = artifacts_dir
        self.operator_action = operator_action or {}

    def run(self, context: PipelineContext) -> ModuleResult:
        dossier_path = resolve_dossier_input(self.dossier_path, context.artifacts)
        if dossier_path is None:
            return ModuleResult(context=context, status="skipped", notes=["reply_sender skipped: dossier_path missing"])

        try:
            payload = load_dossier(dossier_path)
            draft_text = latest_draft_text(payload)
            if not draft_text:
                raise ValueError("latest draft is empty")

            created = timestamp_for_filename()
            cid = case_id(payload)
            outbox_dir = resolve_project_path(self.artifacts_dir) / "mock_outbox" / safe_case_dir_name(cid)
            outbox_dir.mkdir(parents=True, exist_ok=True)
            reply_subject = subject(payload)
            if reply_subject and not reply_subject.lower().startswith("re:"):
                reply_subject = f"Re: {reply_subject}"

            reply_payload = {
                "status": "approved_mock_not_sent",
                "to": sender(payload),
                "subject": reply_subject,
                "uid": resolve_uid(payload),
                "case_id": cid,
                "thread_id": thread_id(payload),
                "operator_action": self.operator_action,
                "final_draft_text": draft_text,
                "draft_revision": latest_draft_module(payload).get("latest_revision"),
                "timestamp": created,
                "source_dossier_path": str(dossier_path),
                "real_email_sent": False,
            }
            json_path = outbox_dir / f"reply_{created}.json"
            md_path = outbox_dir / f"reply_{created}.md"
            write_json(json_path, reply_payload)
            md_path.write_text(_render_mock_reply(reply_payload), encoding="utf-8")

            reply_payload["mock_reply_refs"] = [str(md_path), str(json_path)]
            modules = payload.setdefault("modules", {})
            modules[self.name] = reply_payload
            save_dossier(dossier_path, payload)
        except Exception as exc:
            return ModuleResult(context=context, status="error", notes=[f"reply_sender failed: {exc}"])

        refs = [str(dossier_path), *reply_payload["mock_reply_refs"]]
        context.artifacts.setdefault(self.name, []).extend(refs)
        return ModuleResult(
            context=context,
            status="ok",
            notes=[
                "reply_sender created mock_outbox artifact",
                "real_email_sent=False",
            ],
            artifact_refs=refs,
            metrics=reply_payload,
        )


def _render_mock_reply(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Mock reply",
            "",
            f"- status: {payload['status']}",
            f"- to: {payload['to']}",
            f"- subject: {payload['subject']}",
            f"- uid: {payload['uid']}",
            f"- case_id: {payload['case_id']}",
            f"- thread_id: {payload['thread_id']}",
            f"- draft_revision: {payload.get('draft_revision')}",
            f"- timestamp: {payload['timestamp']}",
            f"- source dossier path: {payload['source_dossier_path']}",
            f"- real email sent: {payload['real_email_sent']}",
            "",
            "## Final draft text",
            "",
            str(payload["final_draft_text"]).rstrip(),
            "",
        ]
    )
