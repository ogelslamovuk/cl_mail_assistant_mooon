from __future__ import annotations

from pathlib import Path

from src.pipeline.identity_context_enrichment.module import IdentityContextEnrichmentModule
from src.runners._runner_utils import base_parser, init_context
from src.shared.common.message_dossier import load_message_record
from src.shared.common.paths import resolve_project_path


def _find_latest_candidate(artifacts_dir: str) -> tuple[str, str | None] | None:
    roots = [
        Path(resolve_project_path(artifacts_dir)) / "modules" / "mail_import",
        Path(resolve_project_path(".")),
    ]

    candidates: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        candidates.extend(root.rglob("message_*.md"))
        candidates.extend(root.rglob("parsed_email_*.json"))

    candidates.sort(key=lambda path: path.stat().st_mtime, reverse=True)

    for parsed_path in candidates:
        try:
            payload = load_message_record(parsed_path)
        except Exception:
            continue
        message_id = str(payload.get("message_id", "") or "")
        if message_id.startswith("__bootstrap_cursor__"):
            continue
        attachment_report = _find_attachment_report(parsed_path)
        return str(parsed_path), str(attachment_report) if attachment_report else None

    return None


def _find_attachment_report(parsed_email_path: Path) -> Path | None:
    if parsed_email_path.suffix.lower() == ".md":
        return parsed_email_path
    uid = parsed_email_path.stem.replace("parsed_email_", "").replace("message_", "")
    attachment_candidate = parsed_email_path.with_name(f"message_{uid}.md")
    if attachment_candidate.exists():
        return attachment_candidate
    legacy_candidate = parsed_email_path.with_name(f"attachment_extraction_report_{uid}.json")
    if legacy_candidate.exists():
        return legacy_candidate
    return None


def _print_summary(result) -> None:
    metrics = result.metrics or {}
    print("[identity_context_enrichment] status=", result.status)
    print(
        "[identity_context_enrichment] "
        f"uid={metrics.get('uid', '')} "
        f"subject={metrics.get('subject', '') or '<empty>'} "
        f"selected_lookup_email={metrics.get('selected_lookup_email', '') or '<empty>'}"
    )
    print(
        "[identity_context_enrichment] "
        f"ticket_db_status={metrics.get('ticket_db_status', '')} "
        f"ticket_db_found_rows={metrics.get('ticket_db_found_rows', 0)} "
        f"ticket_db_rescue_candidates={metrics.get('ticket_db_rescue_candidates', 0)}"
    )

    resolved = metrics.get("resolved_match") or {}
    if resolved:
        print(
            "[identity_context_enrichment] resolved "
            f"ticket={resolved.get('ticket', '')} "
            f"theater={resolved.get('theater', '')} "
            f"event={resolved.get('event', '')}"
        )

    result_path = metrics.get("result_path", "")
    debug_path = metrics.get("debug_path", "")
    if result_path:
        print(f"[identity_context_enrichment] result_path={result_path}")
    if debug_path:
        print(f"[identity_context_enrichment] debug_path={debug_path}")

    if result.status == "error":
        for note in result.notes:
            print(f"[identity_context_enrichment] error {note}")


def main() -> None:
    parser = base_parser("Run identity_context_enrichment module in isolation")
    parser.add_argument("--parsed-email-path")
    parser.add_argument("--attachment-report-path")
    args = parser.parse_args()

    parsed_email_path = str(args.parsed_email_path or "").strip()
    attachment_report_path = str(args.attachment_report_path or "").strip() or None

    if not parsed_email_path:
        discovered = _find_latest_candidate(args.artifacts_dir)
        if not discovered:
            raise SystemExit("No suitable parsed_email found")
        parsed_email_path, discovered_attachment = discovered
        if not attachment_report_path:
            attachment_report_path = discovered_attachment

    context = init_context(run_id=args.run_id)
    result = IdentityContextEnrichmentModule(
        parsed_email_path=str(resolve_project_path(parsed_email_path)),
        attachment_report_path=str(resolve_project_path(attachment_report_path)) if attachment_report_path else None,
    ).run(context)

    _print_summary(result)

    if result.status == "error":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
