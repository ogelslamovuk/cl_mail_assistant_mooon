from __future__ import annotations

from src.pipeline.pre_triage.module import PreTriageModule
from src.runners._runner_utils import base_parser, init_context, persist_single_module_result


def main() -> None:
    parser = base_parser("Run pre_triage module in isolation")
    args = parser.parse_args()

    context = init_context(run_id=args.run_id)
    result = PreTriageModule().run(context)

    persist_single_module_result(
        artifacts_dir=args.artifacts_dir,
        run_id=args.run_id,
        module_name="pre_triage",
        payload={
            "status": result.status,
            "notes": result.notes,
            "artifact_refs": result.artifact_refs,
        },
    )


if __name__ == "__main__":
    main()
