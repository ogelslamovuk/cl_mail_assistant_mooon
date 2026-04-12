from __future__ import annotations

from src.shared.contracts.module_contract import ModuleResult
from src.shared.models.pipeline_context import PipelineContext


class RouterModule:
    name = "router"

    def run(self, context: PipelineContext) -> ModuleResult:
        notes = ["Skeleton module executed."]
        return ModuleResult(context=context, status="ok", notes=notes, artifact_refs=[])
