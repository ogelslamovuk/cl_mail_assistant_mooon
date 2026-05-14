from __future__ import annotations

from src.pipeline.operator_flow import (
    build_draft_revision,
    latest_draft_text,
    load_dossier,
    resolve_dossier_input,
    save_dossier,
)
from src.shared.contracts.module_contract import ModuleResult
from src.shared.models.pipeline_context import PipelineContext


class DraftBuilderModule:
    name = "draft_builder"

    def __init__(
        self,
        dossier_path: str | None = None,
        operator_comment: str = "",
        revision_reason: str = "initial",
    ) -> None:
        self.dossier_path = dossier_path
        self.operator_comment = operator_comment
        self.revision_reason = revision_reason

    def run(self, context: PipelineContext) -> ModuleResult:
        dossier_path = resolve_dossier_input(self.dossier_path, context.artifacts)
        if dossier_path is None:
            return ModuleResult(context=context, status="skipped", notes=["draft_builder skipped: dossier_path missing"])

        try:
            payload = load_dossier(dossier_path)
            draft_payload = build_draft_revision(
                payload,
                dossier_path=str(dossier_path),
                operator_comment=self.operator_comment,
                revision_reason=self.revision_reason,
            )
            save_dossier(dossier_path, payload)
        except Exception as exc:
            return ModuleResult(context=context, status="error", notes=[f"draft_builder failed: {exc}"])

        context.artifacts.setdefault(self.name, []).append(str(dossier_path))
        context.draft = None
        notes = [
            f"draft_builder processed uid={draft_payload['uid']}",
            f"status={draft_payload.get('status', 'ok')}",
            f"revision={draft_payload.get('latest_revision')}",
            "real_email_sent=False",
        ]
        return ModuleResult(
            context=context,
            status="ok",
            notes=notes,
            artifact_refs=[str(dossier_path)],
            metrics={
                "dossier_path": str(dossier_path),
                "status": draft_payload.get("status", "ok"),
                "skip_reason": draft_payload.get("skip_reason", ""),
                "latest_revision": draft_payload.get("latest_revision"),
                "draft_text": latest_draft_text(payload),
                "real_email_sent": False,
            },
        )
