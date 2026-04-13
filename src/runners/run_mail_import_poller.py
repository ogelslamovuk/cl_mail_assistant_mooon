from __future__ import annotations

import time
from uuid import uuid4

from src.layers.config.local_yaml_config_store import LocalYamlConfigStore
from src.layers.state.import_registry_store import ImportRegistryStore
from src.pipeline.mail_import.module import MailImportModule
from src.runners._runner_utils import base_parser, init_context
def main() -> None:
    parser = base_parser("Run background mail_import IMAP poller")
    parser.add_argument("--poll-interval-sec", type=int)
    args = parser.parse_args()

    config_store = LocalYamlConfigStore()
    mail_import_config = config_store.get_section("mail_import")
    source_mode = str(mail_import_config.get("mode", "fixture")).lower()
    if source_mode != "imap":
        raise SystemExit("mail_import poller supports only mode=imap")

    if not bool(mail_import_config.get("enabled", True)):
        print("[mail_import_poller] mail_import is disabled by config; exiting.")
        return

    poll_interval_sec = args.poll_interval_sec
    if poll_interval_sec is None:
        poll_interval_sec = int(mail_import_config.get("poll_interval_sec", 3))
    if poll_interval_sec <= 0:
        raise SystemExit("poll_interval_sec must be > 0")

    run_options = {
        "mode": "imap",
        "fixture_path": None,
    }

    registry_store = ImportRegistryStore(base_dir=args.artifacts_dir)
    registry_path = registry_store.registry_path
    print(
        "[mail_import_poller] started "
        f"mode=imap poll_interval_sec={poll_interval_sec} registry={registry_path}"
    )

    cycle = 0
    try:
        while True:
            cycle += 1
            cycle_run_id = f"run-{uuid4().hex[:8]}"
            before_count = len(registry_store.read_all())
            print(f"[mail_import_poller] cycle={cycle} run_id={cycle_run_id} started")

            try:
                context = init_context(run_id=cycle_run_id)
                result = MailImportModule(
                    config=mail_import_config,
                    artifacts_dir=args.artifacts_dir,
                    run_options=run_options,
                ).run(context)
            except Exception as exc:
                print(f"[mail_import_poller] cycle={cycle} exception={exc}")
                time.sleep(poll_interval_sec)
                continue

            after_count = len(registry_store.read_all())
            inserted_rows = max(0, after_count - before_count)

            processed_count = int(result.metrics.get("processed_count", 0))
            new_count = int(result.metrics.get("new_count", inserted_rows))
            imports = result.metrics.get("imports", [])
            duplicate_count = max(0, len(imports) - new_count)
            empty_result = processed_count == 0

            if result.status == "error":
                notes = "; ".join(result.notes) if result.notes else "unknown error"
                print(f"[mail_import_poller] cycle={cycle} status=error details={notes}")
            elif empty_result:
                print(
                    "[mail_import_poller] "
                    f"cycle={cycle} status=ok processed_count=0 empty_result=true registry={registry_path}"
                )
            else:
                print(
                    "[mail_import_poller] "
                    f"cycle={cycle} status=ok processed_count={processed_count} "
                    f"new_count={new_count} duplicate_count={duplicate_count} "
                    f"registry={registry_path}"
                )

            time.sleep(poll_interval_sec)
    except KeyboardInterrupt:
        print("[mail_import_poller] stop requested via Ctrl+C")
    finally:
        print("[mail_import_poller] stopped")


if __name__ == "__main__":
    main()
