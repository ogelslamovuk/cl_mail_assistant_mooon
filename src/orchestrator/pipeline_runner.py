from __future__ import annotations

from src.layers.artifacts.artifact_store import ArtifactStore
from src.layers.artifacts.logger import get_logger
from src.orchestrator.pipeline_registry import MODULE_REGISTRY, PIPELINE_ORDER
from src.shared.common.paths import resolve_project_path
from src.shared.contracts.module_contract import ModuleResult
from src.shared.models.pipeline_context import PipelineContext


class PipelineRunner:
    def __init__(self, artifact_dir: str = "artifacts") -> None:
        self.artifact_store = ArtifactStore(base_dir=artifact_dir)
        self.logger = get_logger("pipeline_runner", log_dir=str(resolve_project_path(artifact_dir) / "logs"))

    def _resolve_steps(
        self,
        from_step: str | None = None,
        to_step: str | None = None,
        steps: list[str] | None = None,
    ) -> list[str]:
        if steps:
            return steps

        selected = PIPELINE_ORDER
        if from_step:
            selected = selected[selected.index(from_step) :]
        if to_step:
            selected = selected[: selected.index(to_step) + 1]
        return selected

    def run(
        self,
        context: PipelineContext,
        from_step: str | None = None,
        to_step: str | None = None,
        steps: list[str] | None = None,
    ) -> PipelineContext:
        planned_steps = self._resolve_steps(from_step=from_step, to_step=to_step, steps=steps)

        for step in planned_steps:
            module = MODULE_REGISTRY[step]()
            self.logger.info("Running step: %s", step)
            result: ModuleResult = module.run(context)
            context = result.context

            artifact_payload = {
                "step": step,
                "status": result.status,
                "notes": result.notes,
                "artifact_refs": result.artifact_refs,
            }
            ref = self.artifact_store.write_module_output(context.run_id, step, artifact_payload)
            context.artifacts.setdefault(step, []).append(ref)

        self.artifact_store.write_run_snapshot(context.run_id, context)
        return context
