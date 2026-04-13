from __future__ import annotations

from src.layers.config.local_yaml_config_store import LocalYamlConfigStore
from src.pipeline.mail_import.module import MailImportModule
from src.runners._runner_utils import base_parser, init_context, persist_single_module_result


def main() -> None:
    parser = base_parser("Run mail_import module in isolation")
    parser.add_argument("--config", default="config.local.yaml")
    parser.add_argument("--mode", choices=["fixture", "imap"])
    parser.add_argument("--fixture-path")
    parser.add_argument("--max-messages-per-run", type=int)
    parser.add_argument("--search-criteria")
    parser.add_argument("--mailbox")
    parser.add_argument("--readonly", action="store_true")
    parser.add_argument("--readwrite", action="store_true")
    args = parser.parse_args()

    config_store = LocalYamlConfigStore(path=args.config)
    mail_import_config = config_store.get_section("mail_import")

    readonly_override = None
    if args.readonly:
        readonly_override = True
    if args.readwrite:
        readonly_override = False

    cli_overrides = {
        "mode": args.mode,
        "fixture_path": args.fixture_path,
        "max_messages_per_run": args.max_messages_per_run,
        "search_criteria": args.search_criteria,
        "mailbox": args.mailbox,
        "readonly": readonly_override,
    }

    context = init_context(run_id=args.run_id)
    result = MailImportModule(
        config=mail_import_config,
        artifacts_dir=args.artifacts_dir,
        run_options=cli_overrides,
    ).run(context)

    persist_single_module_result(
        artifacts_dir=args.artifacts_dir,
        run_id=args.run_id,
        module_name="mail_import",
        payload={
            "status": result.status,
            "notes": result.notes,
            "artifact_refs": result.artifact_refs,
            "message_id": result.context.message.message_id if result.context.message else None,
        },
    )


if __name__ == "__main__":
    main()
