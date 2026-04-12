from __future__ import annotations

from pathlib import Path
from typing import Any

from src.shared.common.io import write_json


class ArtifactStore:
    def __init__(self, base_dir: str = "artifacts") -> None:
        self.base_dir = Path(base_dir)

    def write_module_output(self, run_id: str, module_name: str, payload: Any) -> str:
        target = self.base_dir / "modules" / module_name / run_id / "output.json"
        return write_json(target, payload)

    def write_run_snapshot(self, run_id: str, payload: Any) -> str:
        target = self.base_dir / "runs" / run_id / "pipeline_context.json"
        return write_json(target, payload)
