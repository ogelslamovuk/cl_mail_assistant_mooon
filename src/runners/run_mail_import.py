from __future__ import annotations

from src.layers.artifacts.artifact_store import ArtifactStore
from src.layers.config.local_yaml_config_store import LocalYamlConfigStore
from src.pipeline.mail_import.module import MailImportModule
from src.runners._runner_utils import base_parser, init_context
from src.shared.common.paths import resolve_project_path


def main() -> None:
    parser = base_parser("Run mail_import module in isolation")
    parser.add_argument("--mode", choices=["fixture", "imap"])
    parser.add_argument("--fixture-path")
    parser.add_argument("--max-messages-per-run", type=int)
    parser.add_argument("--search-criteria")
    parser.add_argument("--mailbox")
    parser.add_argument("--readonly", action="store_true")
    parser.add_argument("--readwrite", action="store_true")
    args = parser.parse_args()

    config_store = LocalYamlConfigStore()
    mail_import_config = config_store.get_section("mail_import")

    readonly_override = None
    if args.readonly:
        readonly_override = True
    if args.readwrite:
        readonly_override = False

    cli_overrides = {
        "mode": args.mode,
        "fixture_path": str(resolve_project_path(args.fixture_path)) if args.fixture_path else None,
        "max_messages_per_run": args.max_messages_per_run,
        "search_criteria": args.search_criteria,
        "mailbox": args.mailbox,
        "readonly": readonly_override,
    }

    context = init_context(run_id=args.run_id)
    result = MailImportModule(
        config=mail_import_config,
        artifacts_dir=str(resolve_project_path(args.artifacts_dir)),
        run_options=cli_overrides,
    ).run(context)

    imports = result.metrics.get("imports", [])
    processed_count = int(result.metrics.get("processed_count", 0))
    new_count = int(result.metrics.get("new_count", 0))
    registry_path = str(result.metrics.get("registry_path", ""))
    print(f"[mail_import] processed_count={processed_count} new_count={new_count}")
    for item in imports:
        if item.get("status") == "duplicate":
            print(
                "[mail_import] duplicate "
                f"import_id={item.get('import_id')} row={item.get('row_number')} "
                f"message_id={item.get('message_id')} status=duplicate"
            )
        else:
            print(
                "[mail_import] imported "
                f"import_id={item.get('import_id')} row={item.get('row_number')} "
                f"message_id={item.get('message_id')} status={item.get('status')}"
            )
        print(
            "[mail_import] artifacts "
            f"raw={item.get('raw_path')} "
            f"parsed_email={item.get('parsed_email_path')}"
        )
    if registry_path:
        print(f"[mail_import] registry={registry_path}")

    store = ArtifactStore(base_dir=str(resolve_project_path(args.artifacts_dir)))
    module_result_ref = store.write_module_output(
        run_id=args.run_id,
        module_name="mail_import",
        payload={
            "status": result.status,
            "notes": result.notes,
            "artifact_refs": result.artifact_refs,
            "message_id": result.context.message.message_id if result.context.message else None,
            "imported_count": processed_count,
            "new_count": new_count,
            "imports": imports,
            "registry_path": registry_path,
        },
    )

    print("mail_import finished")
    print(f"status: {result.status}")
    if result.context.message:
        print(f"message_id: {result.context.message.message_id}")
    else:
        print("message_id: <none>")

    if result.notes:
        print("notes:")
        for note in result.notes:
            print(f"  - {note}")

    print("artifacts:")
    for ref in result.artifact_refs:
        print(f"  - {ref}")
    print(f"  - {module_result_ref}")

    if result.status == "error":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
