from __future__ import annotations

from src.pipeline.operator_actions.module import OperatorActionsModule
from src.runners._runner_utils import base_parser, init_context, persist_single_module_result


def main() -> None:
    parser = base_parser("Run operator_actions module in isolation")
    parser.add_argument("--dossier-path", default=None)
    parser.add_argument("--action", default="")
    parser.add_argument("--callback-data", default="")
    parser.add_argument("--operator-comment", default="")
    parser.add_argument("--operator-telegram-id", default="mock_operator")
    parser.add_argument("--operator-username", default="mock_operator")
    args = parser.parse_args()

    context = init_context(run_id=args.run_id)
    result = OperatorActionsModule(
        dossier_path=args.dossier_path,
        artifacts_dir=args.artifacts_dir,
        action=args.action,
        callback_data=args.callback_data,
        operator_comment=args.operator_comment,
        operator_telegram_id=args.operator_telegram_id,
        operator_username=args.operator_username,
    ).run(context)

    persist_single_module_result(
        artifacts_dir=args.artifacts_dir,
        run_id=args.run_id,
        module_name="operator_actions",
        payload={
            "status": result.status,
            "notes": result.notes,
            "artifact_refs": result.artifact_refs,
            "metrics": result.metrics,
        },
    )


if __name__ == "__main__":
    main()
