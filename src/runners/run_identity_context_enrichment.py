from __future__ import annotations

from src.pipeline.identity_context_enrichment.module import IdentityContextEnrichmentModule
from src.runners._runner_utils import base_parser, init_context, persist_single_module_result


def main() -> None:
    parser = base_parser("Run identity_context_enrichment module in isolation")
    args = parser.parse_args()

    context = init_context(run_id=args.run_id)
    result = IdentityContextEnrichmentModule().run(context)

    persist_single_module_result(
        artifacts_dir=args.artifacts_dir,
        run_id=args.run_id,
        module_name="identity_context_enrichment",
        payload={
            "status": result.status,
            "notes": result.notes,
            "artifact_refs": result.artifact_refs,
        },
    )


if __name__ == "__main__":
    main()
