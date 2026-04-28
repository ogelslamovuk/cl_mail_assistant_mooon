from __future__ import annotations

from pathlib import Path

from src.pipeline.attachment_extraction.module import AttachmentExtractionModule
from src.runners._runner_utils import base_parser, init_context
from src.shared.common.message_dossier import load_message_record
from src.shared.common.paths import resolve_project_path


def _find_latest_candidate(artifacts_dir: str) -> tuple[str, str] | None:
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
        inventory = payload.get("attachments_inventory") or []
        if not inventory:
            continue
        raw_path = str(payload.get("raw_path", "") or "").strip()
        if raw_path and Path(raw_path).exists():
            return str(parsed_path), raw_path
        stem_uid = parsed_path.stem.replace("parsed_email_", "").replace("message_", "")
        raw_candidate = parsed_path.with_name(f"raw_email_{stem_uid}.eml")
        if raw_candidate.exists():
            return str(parsed_path), str(raw_candidate)

    return None


def _print_summary(result) -> None:
    metrics = result.metrics or {}
    print("[attachment_extraction] status=", result.status)
    print(
        "[attachment_extraction] "
        f"uid={metrics.get('uid', '')} "
        f"subject={metrics.get('subject', '') or '<empty>'} "
        f"items_count={metrics.get('items_count', 0)}"
    )

    for item in metrics.get("items", []):
        role = "inline" if item.get("is_inline") else "attachment"
        text_found = "yes" if bool(item.get("text_found")) else "no"
        preview = str(item.get("text_preview", "") or "")[:120]
        print(
            "[attachment_extraction] item "
            f"filename={item.get('filename_saved') or item.get('filename_original') or '<empty>'} "
            f"content_type={item.get('content_type', '')} "
            f"role={role} "
            f"text_found={text_found} "
            f"method={item.get('extraction_method', '')} "
            f"preview={preview or '<empty>'}"
        )

    if result.status == "error":
        for note in result.notes:
            print(f"[attachment_extraction] error {note}")


def main() -> None:
    parser = base_parser("Run attachment_extraction module in isolation")
    parser.add_argument("--parsed-email-path")
    parser.add_argument("--raw-email-path")
    args = parser.parse_args()

    parsed_email_path = str(args.parsed_email_path or "").strip()
    raw_email_path = str(args.raw_email_path or "").strip() or None

    if not parsed_email_path:
        discovered = _find_latest_candidate(args.artifacts_dir)
        if not discovered:
            raise SystemExit("No suitable parsed_email/raw_email pair found")
        parsed_email_path, discovered_raw = discovered
        if not raw_email_path:
            raw_email_path = discovered_raw

    context = init_context(run_id=args.run_id)
    result = AttachmentExtractionModule(
        parsed_email_path=str(resolve_project_path(parsed_email_path)),
        raw_email_path=str(resolve_project_path(raw_email_path)) if raw_email_path else None,
    ).run(context)

    _print_summary(result)

    if result.status == "error":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
