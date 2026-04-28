from __future__ import annotations

from pathlib import Path

from src.pipeline.case_thread_binding.module import CaseThreadBindingModule
from src.runners._runner_utils import base_parser, init_context
from src.shared.common.message_dossier import load_message_record
from src.shared.common.paths import resolve_project_path


def _find_latest_candidate(artifacts_dir: str) -> str | None:
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
        return str(parsed_path)

    return None


def _print_summary(result) -> None:
    metrics = result.metrics or {}
    print("[case_thread_binding] status=", result.status)
    print(
        "[case_thread_binding] "
        f"uid={metrics.get('uid', '')} "
        f"message_id={metrics.get('message_id', '') or '<empty>'}"
    )
    print(
        "[case_thread_binding] "
        f"case_id={metrics.get('case_id', '') or '<empty>'} "
        f"thread_id={metrics.get('thread_id', '') or '<empty>'} "
        f"rule={metrics.get('binding_rule', '') or '<empty>'}"
    )
    print(
        "[case_thread_binding] "
        f"matched_message_id={metrics.get('matched_message_id', '') or '<empty>'} "
        f"thread_messages_count={metrics.get('thread_messages_count', 0)} "
        f"created={metrics.get('created', False)}"
    )

    registry_path = metrics.get("registry_path", "")
    binding_path = metrics.get("binding_path", "")
    if registry_path:
        print(f"[case_thread_binding] registry_path={registry_path}")
    if binding_path:
        print(f"[case_thread_binding] binding_path={binding_path}")

    if result.status in {"error", "skipped"}:
        for note in result.notes:
            print(f"[case_thread_binding] note {note}")


def main() -> None:
    parser = base_parser("Run case_thread_binding module in isolation")
    parser.add_argument("--parsed-email-path")
    args = parser.parse_args()

    parsed_email_path = str(args.parsed_email_path or "").strip()
    if not parsed_email_path:
        discovered = _find_latest_candidate(args.artifacts_dir)
        if not discovered:
            raise SystemExit("No suitable parsed_email found")
        parsed_email_path = discovered

    context = init_context(run_id=args.run_id)
    result = CaseThreadBindingModule(
        parsed_email_path=str(resolve_project_path(parsed_email_path)),
        artifacts_dir=args.artifacts_dir,
    ).run(context)

    _print_summary(result)

    if result.status == "error":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
