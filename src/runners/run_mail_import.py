from __future__ import annotations

import sys
from pathlib import Path

from src.layers.artifacts.artifact_store import ArtifactStore
from src.layers.config.local_yaml_config_store import LocalYamlConfigStore
from src.pipeline.mail_import.module import MailImportModule
from src.runners._runner_utils import base_parser, init_context


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _resolve_from_project_root(raw_path: str | None) -> str | None:
    if not raw_path:
        return None

    path = Path(raw_path)
    if path.is_absolute():
        return str(path)

    return str((PROJECT_ROOT / path).resolve())


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

    artifacts_dir = _resolve_from_project_root(args.artifacts_dir) or str((PROJECT_ROOT / "artifacts").resolve())

    config_store = LocalYamlConfigStore()
    mail_import_config = config_store.get_section("mail_import")

    readonly_override = None
    if args.readonly:
        readonly_override = True
    if args.readwrite:
        readonly_override = False

    cli_overrides = {
        "mode": args.mode,
        "fixture_path": _resolve_from_project_root(args.fixture_path),
        "max_messages_per_run": args.max_messages_per_run,
        "search_criteria": args.search_criteria,
        "mailbox": args.mailbox,
        "readonly": readonly_override,
    }

    context = init_context(run_id=args.run_id)
    result = MailImportModule(
        config=mail_import_config,
        artifacts_dir=artifacts_dir,
        run_options=cli_overrides,
    ).run(context)

    store = ArtifactStore(base_dir=artifacts_dir)
    module_result_ref = store.write_module_output(
        run_id=args.run_id,
        module_name="mail_import",
        payload={
            "status": result.status,
            "notes": result.notes,
            "artifact_refs": result.artifact_refs,
            "message_id": result.context.message.message_id if result.context.message else None,
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
