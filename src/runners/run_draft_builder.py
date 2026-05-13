from __future__ import annotations

from src.pipeline.draft_builder.module import DraftBuilderModule
from src.runners._runner_utils import base_parser, init_context, persist_single_module_result


def main() -> None:
    parser = base_parser("Run draft_builder module in isolation")
    parser.add_argument("--dossier-path", default=None)
    parser.add_argument("--operator-comment", default="")
    parser.add_argument("--revision-reason", default="initial")
    args = parser.parse_args()

    context = init_context(run_id=args.run_id)
    result = DraftBuilderModule(
        dossier_path=args.dossier_path,
        operator_comment=args.operator_comment,
        revision_reason=args.revision_reason,
    ).run(context)

    persist_single_module_result(
        artifacts_dir=args.artifacts_dir,
        run_id=args.run_id,
        module_name="draft_builder",
        payload={
            "status": result.status,
            "notes": result.notes,
            "artifact_refs": result.artifact_refs,
            "metrics": result.metrics,
        },
    )


if __name__ == "__main__":
    main()
