from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from src.layers.config.local_yaml_config_store import LocalYamlConfigStore
from src.layers.state.import_registry_store import ImportRegistryStore
from src.pipeline.attachment_extraction.module import AttachmentExtractionModule
from src.pipeline.mail_import.module import MailImportModule
from src.runners._runner_utils import base_parser, init_context
from src.shared.common.paths import resolve_project_path


def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _read_sender_subject_from_parsed_email_path(parsed_email_path: str) -> tuple[str, str]:
    if not parsed_email_path:
        return "", ""
    try:
        path = Path(parsed_email_path)
        if not path.exists():
            return "", ""
        with path.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        headers = payload.get("headers", {}) if isinstance(payload, dict) else {}
        if not isinstance(headers, dict):
            headers = {}

        sender = str(headers.get("sender", "") or payload.get("sender", "") or "").strip()
        subject = str(headers.get("subject", "") or payload.get("subject", "") or "").strip()
        return sender, subject
    except Exception:
        return "", ""


def _print_attachment_extraction_summary(extraction_metrics: dict) -> None:
    uid = str(extraction_metrics.get("uid", "") or "")
    subject = str(extraction_metrics.get("subject", "") or "")
    items = extraction_metrics.get("items", [])
    print(
        f"[attachment_extraction] {_ts()} uid={uid or '<empty>'} "
        f"subject={subject or '<empty>'} items_count={len(items)}"
    )

    for item in items:
        role = "inline" if bool(item.get("is_inline")) else "attachment"
        text_found = "yes" if bool(item.get("text_found")) else "no"
        preview = str(item.get("text_preview", "") or "")[:120]
        print(
            "[attachment_extraction] item "
            f"filename={item.get('filename_saved') or item.get('filename_original') or '<empty>'} "
            f"content_type={item.get('content_type', '')} "
            f"role={role} text_found={text_found} "
            f"method={item.get('extraction_method', '')} "
            f"preview={preview or '<empty>'}"
        )


def _resolve_sender_subject(import_item: dict) -> tuple[str, str]:
    sender = str(import_item.get("sender", "") or "").strip()
    subject = str(import_item.get("subject", "") or "").strip()

    if sender and subject:
        return sender, subject

    parsed_email_path = str(
        import_item.get("parsed_email_path", "")
        or import_item.get("parsed_message_path", "")
        or ""
    ).strip()
    fallback_sender, fallback_subject = _read_sender_subject_from_parsed_email_path(parsed_email_path)

    if not sender:
        sender = fallback_sender
    if not subject:
        subject = fallback_subject

    return sender, subject


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
        print(f"[mail_import_poller] {_ts()} error mail_import is disabled by config")
        return

    poll_interval_sec = args.poll_interval_sec
    if poll_interval_sec is None:
        poll_interval_sec = int(mail_import_config.get("poll_interval_sec", 3))
    if poll_interval_sec <= 0:
        raise SystemExit("poll_interval_sec must be > 0")

    run_options = {
        "mode": "imap",
        "fixture_path": None,
        "readonly": True,
    }

    normalized_artifacts_dir = str(resolve_project_path(args.artifacts_dir))
    registry_store = ImportRegistryStore(base_dir=normalized_artifacts_dir)
    print(f"[mail_import_poller] {_ts()} started")

    try:
        while True:
            cycle_run_id = f"run-{uuid4().hex[:8]}"
            before_count = len(registry_store.read_all())

            try:
                context = init_context(run_id=cycle_run_id)
                result = MailImportModule(
                    config=mail_import_config,
                    artifacts_dir=normalized_artifacts_dir,
                    run_options=run_options,
                ).run(context)
            except Exception as exc:
                print(f"[mail_import_poller] {_ts()} error {exc}")
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
                print(f"[mail_import_poller] {_ts()} error {notes}")
            elif not empty_result and (new_count > 0 or duplicate_count > 0):
                first_import = imports[0] if imports else {}
                sender, subject = _resolve_sender_subject(first_import)
                sender_display = sender if sender else "<unknown>"
                subject_display = subject if subject else "<empty>"
                print(
                    f"[mail_import_poller] {_ts()} new message caught "
                    f"from={sender_display} subject={subject_display} "
                    f"processed={processed_count} new={new_count} duplicate={duplicate_count}"
                )

                new_items = [item for item in imports if str(item.get("status", "")).lower() == "new"]
                for new_item in new_items:
                    parsed_email_path = str(new_item.get("parsed_email_path", "") or "").strip()
                    raw_email_path = str(new_item.get("raw_path", "") or "").strip()
                    if not parsed_email_path:
                        print(f"[attachment_extraction] {_ts()} skip missing parsed_email_path")
                        continue
                    try:
                        extraction_result = AttachmentExtractionModule(
                            parsed_email_path=parsed_email_path,
                            raw_email_path=raw_email_path or None,
                        ).run(context)
                        if extraction_result.status == "error":
                            notes = "; ".join(extraction_result.notes) if extraction_result.notes else "unknown error"
                            print(f"[attachment_extraction] {_ts()} error {notes}")
                            continue
                        _print_attachment_extraction_summary(extraction_result.metrics)
                    except Exception as extraction_exc:
                        print(f"[attachment_extraction] {_ts()} error {extraction_exc}")

            time.sleep(poll_interval_sec)
    except KeyboardInterrupt:
        print(f"[mail_import_poller] {_ts()} stop requested")
    finally:
        print(f"[mail_import_poller] {_ts()} stopped")


if __name__ == "__main__":
    main()
