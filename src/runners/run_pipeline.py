from __future__ import annotations

import argparse
import uuid

from src.orchestrator.pipeline_runner import PipelineRunner
from src.shared.models.pipeline_context import PipelineContext


def parse_steps(raw: str | None) -> list[str] | None:
    if not raw:
        return None
    return [x.strip() for x in raw.split(",") if x.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run full or partial support-mail pipeline")
    parser.add_argument("--run-id", default=f"run-{uuid.uuid4().hex[:8]}")
    parser.add_argument("--artifacts-dir", default="artifacts")
    parser.add_argument("--from-step", default=None)
    parser.add_argument("--to-step", default=None)
    parser.add_argument("--steps", default=None, help="Comma-separated explicit steps")
    args = parser.parse_args()

    context = PipelineContext(run_id=args.run_id)
    runner = PipelineRunner(artifact_dir=args.artifacts_dir)
    runner.run(
        context,
        from_step=args.from_step,
        to_step=args.to_step,
        steps=parse_steps(args.steps),
    )


if __name__ == "__main__":
    main()
