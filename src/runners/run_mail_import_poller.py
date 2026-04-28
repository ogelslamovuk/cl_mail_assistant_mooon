from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from src.layers.config.local_yaml_config_store import LocalYamlConfigStore
from src.layers.state.import_registry_store import ImportRegistryStore
from src.pipeline.attachment_extraction.module import AttachmentExtractionModule
from src.pipeline.identity_context_enrichment.module import IdentityContextEnrichmentModule
from src.pipeline.case_thread_binding.module import CaseThreadBindingModule
from src.pipeline.mail_import.module import MailImportModule
from src.runners._runner_utils import base_parser, init_context
from src.shared.common.message_dossier import load_message_record
from src.shared.common.paths import resolve_project_path


def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _format_console_datetime(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return "<empty>"
    text = text.replace("T", " ")
    if text.endswith("Z"):
        text = text[:-1].strip()
    if len(text) >= 25 and (text[-6] in {"+", "-"}) and text[-3] == ":":
        text = text[:-6].strip()
    if len(text) >= 19:
        return text[:19]
    return text


def _read_message_fields_from_parsed_email_path(parsed_email_path: str) -> tuple[str, str, str]:
    if not parsed_email_path:
        return "", "", ""
    try:
        path = Path(parsed_email_path)
        if not path.exists():
            return "", "", ""
        payload = load_message_record(path)

        headers = payload.get("headers", {}) if isinstance(payload, dict) else {}
        if not isinstance(headers, dict):
            headers = {}

        sender = str(headers.get("sender", "") or payload.get("sender", "") or "").strip()
        subject = str(headers.get("subject", "") or payload.get("subject", "") or "").strip()
        sent_at = str(
            headers.get("sent_at", "")
            or headers.get("date", "")
            or payload.get("sent_at", "")
            or payload.get("date", "")
            or ""
        ).strip()
        return sender, subject, sent_at
    except Exception:
        return "", "", ""


def _resolve_message_fields(import_item: dict) -> tuple[str, str, str]:
    sender = str(import_item.get("sender", "") or "").strip()
    subject = str(import_item.get("subject", "") or "").strip()
    sent_at = str(
        import_item.get("sent_at", "")
        or import_item.get("date", "")
        or import_item.get("message_date", "")
        or ""
    ).strip()

    if sender and subject and sent_at:
        return sender, subject, sent_at

    parsed_email_path = str(
        import_item.get("parsed_email_path", "")
        or import_item.get("parsed_message_path", "")
        or ""
    ).strip()
    fallback_sender, fallback_subject, fallback_sent_at = _read_message_fields_from_parsed_email_path(parsed_email_path)

    if not sender:
        sender = fallback_sender
    if not subject:
        subject = fallback_subject
    if not sent_at:
        sent_at = fallback_sent_at

    return sender, subject, sent_at


def _short_note(notes: list[str] | None) -> str:
    if not notes:
        return ""
    for note in notes:
        text = str(note or "").strip()
        if not text:
            continue
        if text.startswith("identity_context_enrichment processed uid="):
            continue
        if text.startswith("ticket_db_status="):
            continue
        if text.startswith("crm_users_status="):
            continue
        if text.startswith("payment_refund_status="):
            continue
        return text
    return ""


def _truncate_console_value(value: str, limit: int = 100) -> str:
    cleaned = " ".join(str(value or "").split())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 1] + "…"


def _resolve_uid_from_item(new_item: dict, extraction_result, enrichment_result, binding_result=None) -> str:
    uid = str(new_item.get("uid", "") or "").strip()
    if uid:
        return uid
    for result in (extraction_result, enrichment_result, binding_result):
        if result is None:
            continue
        metrics = getattr(result, "metrics", {}) or {}
        uid = str(metrics.get("uid", "") or "").strip()
        if uid:
            return uid
    return "<empty>"


def _build_attachment_extraction_brief(extraction_result) -> str:
    if extraction_result is None:
        return "attach=<not-run>"
    if getattr(extraction_result, "status", "") == "error":
        note = _short_note(getattr(extraction_result, "notes", []))
        return f"attach=error{f'({note})' if note else ''}"

    metrics = getattr(extraction_result, "metrics", {}) or {}
    items = metrics.get("items", []) or []
    text_found_count = 0
    for item in items:
        if bool(item.get("text_found")):
            text_found_count += 1
    return f"attach={len(items)}/{text_found_count}"


def _build_identity_context_enrichment_brief(enrichment_result) -> str:
    if enrichment_result is None:
        return "enrich=<not-run>"
    if getattr(enrichment_result, "status", "") == "error":
        note = _short_note(getattr(enrichment_result, "notes", []))
        return f"enrich=error{f'({note})' if note else ''}"

    metrics = getattr(enrichment_result, "metrics", {}) or {}
    ticket_db_status = str(metrics.get("ticket_db_status", "") or "") or "<empty>"
    selected_lookup_email = str(metrics.get("selected_lookup_email", "") or "")
    resolved = metrics.get("resolved_match") or {}
    ticket = str(resolved.get("ticket", "") or "")

    brief = f"enrich={ticket_db_status}"
    if selected_lookup_email:
        brief += f" lookup={selected_lookup_email}"
    if ticket:
        brief += f" ticket={ticket}"

    note = str(metrics.get("note", "") or "").strip() or _short_note(getattr(enrichment_result, "notes", []))
    if note and note not in {f"ticket_db_status={ticket_db_status}", ""}:
        brief += f" note={note}"
    return brief




def _build_case_thread_binding_brief(binding_result) -> str:
    if binding_result is None:
        return "bind=<not-run>"
    if getattr(binding_result, "status", "") == "error":
        note = _short_note(getattr(binding_result, "notes", []))
        return f"bind=error{f'({note})' if note else ''}"

    metrics = getattr(binding_result, "metrics", {}) or {}
    status = str(metrics.get("status", "") or "ok")
    case_id = str(metrics.get("case_id", "") or "")
    thread_id = str(metrics.get("thread_id", "") or "")
    rule = str(metrics.get("binding_rule", "") or "")
    created = metrics.get("created")

    brief = f"bind={status}"
    if case_id:
        brief += f" case={case_id}"
    if thread_id:
        brief += f" thread={thread_id}"
    if rule:
        brief += f" rule={rule}"
    if created is not None:
        brief += f" created={'yes' if bool(created) else 'no'}"
    return brief

def _print_compact_message_summary(new_item: dict, extraction_result, enrichment_result, binding_result=None) -> None:
    sender, subject, sent_at = _resolve_message_fields(new_item)
    uid = _resolve_uid_from_item(new_item, extraction_result, enrichment_result, binding_result)
    sender_display = _truncate_console_value(sender or "<unknown>", 60)
    subject_display = _truncate_console_value(subject or "<empty>", 100)
    real_display = _format_console_datetime(sent_at)
    attachment_brief = _build_attachment_extraction_brief(extraction_result)
    enrichment_brief = _build_identity_context_enrichment_brief(enrichment_result)
    binding_brief = _build_case_thread_binding_brief(binding_result)

    print(
        f"[mail_import_poller] caught={_ts()} real={real_display} uid={uid} "
        f"from={sender_display} subject=\"{subject_display}\" "
        f"{attachment_brief} {enrichment_brief} {binding_brief}"
    )


def _make_error_result(message: str):
    class _Tmp:
        pass

    tmp = _Tmp()
    tmp.status = "error"
    tmp.notes = [message]
    tmp.metrics = {}
    return tmp


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
    print(f"[mail_import_poller] started={_ts()}")

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
                new_items = [item for item in imports if str(item.get("status", "")).lower() == "new"]
                if not new_items and duplicate_count > 0:
                    print(
                        f"[mail_import_poller] {_ts()} duplicates_only "
                        f"processed={processed_count} new={new_count} duplicate={duplicate_count}"
                    )

                for new_item in new_items:
                    parsed_email_path = str(new_item.get("parsed_email_path", "") or "").strip()
                    raw_email_path = str(new_item.get("raw_path", "") or "").strip()
                    extraction_result = None
                    enrichment_result = None
                    binding_result = None

                    if not parsed_email_path:
                        print(
                            f"[mail_import_poller] {_ts()} uid=<empty> from=<unknown> subject=<empty> "
                            f"attach=skip enrich=skip bind=skip note=missing parsed_email_path"
                        )
                        continue

                    attachment_report_path = None
                    try:
                        extraction_result = AttachmentExtractionModule(
                            parsed_email_path=parsed_email_path,
                            raw_email_path=raw_email_path or None,
                        ).run(context)
                        if extraction_result.status != "error":
                            attachment_report_path = str(extraction_result.metrics.get("report_path", "") or "").strip() or None
                    except Exception as extraction_exc:
                        extraction_result = _make_error_result(str(extraction_exc))

                    try:
                        enrichment_result = IdentityContextEnrichmentModule(
                            parsed_email_path=parsed_email_path,
                            attachment_report_path=attachment_report_path,
                        ).run(context)
                    except Exception as enrichment_exc:
                        enrichment_result = _make_error_result(str(enrichment_exc))

                    try:
                        binding_result = CaseThreadBindingModule(
                            parsed_email_path=parsed_email_path,
                            artifacts_dir=normalized_artifacts_dir,
                        ).run(context)
                    except Exception as binding_exc:
                        binding_result = _make_error_result(str(binding_exc))

                    _print_compact_message_summary(new_item, extraction_result, enrichment_result, binding_result)

            time.sleep(poll_interval_sec)
    except KeyboardInterrupt:
        print(f"[mail_import_poller] stop_requested={_ts()}")
    finally:
        print(f"[mail_import_poller] stopped={_ts()}")


if __name__ == "__main__":
    main()
