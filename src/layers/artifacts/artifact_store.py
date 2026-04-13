from __future__ import annotations

from typing import Any

from src.shared.common.io import write_json
from src.shared.common.paths import resolve_project_path


class ArtifactStore:
    def __init__(self, base_dir: str = "artifacts") -> None:
        self.base_dir = resolve_project_path(base_dir)

    def write_module_output(self, run_id: str, module_name: str, payload: Any) -> str:
        target = self.base_dir / "modules" / module_name / run_id / "output.json"
        return write_json(target, payload)

    def write_run_snapshot(self, run_id: str, payload: Any) -> str:
        target = self.base_dir / "runs" / run_id / "pipeline_context.json"
        return write_json(target, payload)
