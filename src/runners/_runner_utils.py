from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path
from typing import Any

from src.layers.artifacts.artifact_store import ArtifactStore
from src.shared.common.paths import artifacts_dir, resolve_project_path
from src.shared.models.pipeline_context import PipelineContext


def base_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--run-id", default=f"run-{uuid.uuid4().hex[:8]}")
    parser.add_argument("--artifacts-dir", default=str(artifacts_dir()))
    return parser


def init_context(run_id: str) -> PipelineContext:
    return PipelineContext(run_id=run_id)


def load_context_input(path: str) -> dict[str, Any]:
    with resolve_project_path(path).open("r", encoding="utf-8") as f:
        payload = json.load(f)
    if not isinstance(payload, dict):
        raise ValueError("Input JSON must be an object")
    return payload


def persist_single_module_result(artifacts_dir: str, run_id: str, module_name: str, payload: dict) -> None:
    store = ArtifactStore(base_dir=artifacts_dir)
    store.write_module_output(run_id=run_id, module_name=module_name, payload=payload)
