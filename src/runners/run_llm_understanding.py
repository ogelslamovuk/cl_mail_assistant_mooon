from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path

from src.pipeline.llm_understanding.module import LlmUnderstandingModule
from src.shared.common.paths import resolve_project_path
from src.shared.models.pipeline_context import PipelineContext


def main() -> None:
    parser = argparse.ArgumentParser(description="Run llm_understanding module in isolation")
    parser.add_argument("--run-id", default=f"run-{uuid.uuid4().hex[:8]}")
    parser.add_argument("--dossier-path", required=True)
    parser.add_argument("--config-path", default="config/structured_understanding.xlsx")
    parser.add_argument("--output-path", default="")
    args = parser.parse_args()

    dossier_path = resolve_project_path(args.dossier_path)
    config_path = resolve_project_path(args.config_path)
    context = PipelineContext(run_id=args.run_id)
    result = LlmUnderstandingModule(dossier_path=str(dossier_path), config_path=str(config_path)).run(context)

    payload = {
        "run_id": args.run_id,
        "status": result.status,
        "notes": result.notes,
        "metrics": result.metrics,
        "artifact_refs": result.artifact_refs,
    }

    if args.output_path:
        output_path = resolve_project_path(args.output_path)
    else:
        output_path = resolve_project_path(f"artifacts/modules/llm_understanding/{args.run_id}/output.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
