from __future__ import annotations

import argparse
import uuid

from src.layers.artifacts.artifact_store import ArtifactStore
from src.shared.models.pipeline_context import PipelineContext


def base_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--run-id", default=f"run-{uuid.uuid4().hex[:8]}")
    parser.add_argument("--artifacts-dir", default="artifacts")
    return parser


def init_context(run_id: str) -> PipelineContext:
    return PipelineContext(run_id=run_id)


def persist_single_module_result(artifacts_dir: str, run_id: str, module_name: str, payload: dict) -> None:
    store = ArtifactStore(base_dir=artifacts_dir)
    store.write_module_output(run_id=run_id, module_name=module_name, payload=payload)
