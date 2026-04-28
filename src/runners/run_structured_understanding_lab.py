from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.pipeline.llm_understanding.module import LlmUnderstandingModule
from src.shared.common.message_dossier import load_message_record
from src.shared.common.paths import resolve_project_path
from src.shared.models.pipeline_context import PipelineContext

DEFAULT_CONFIG_PATH = "config/structured_understanding.xlsx"
STATE_PATH = "artifacts/state/structured_understanding_lab_state.json"
DOSSIER_GLOB = "artifacts/modules/mail_import/run-*/message_*.md"
LIST_LIMIT = 15


@dataclass
class DossierItem:
    index: int
    uid: str
    sent_at: str
    sender: str
    subject: str
    path: Path


def main() -> None:
    selected_path = load_selected_path_from_state()

    while True:
        dossiers = collect_recent_dossiers()
        if not dossiers:
            print("[understanding_lab] dossiers not found in artifacts/modules/mail_import")
            return

        print_recent_dossiers(dossiers)
        selected_item = find_selected_item(dossiers, selected_path)
        selected_item = choose_item(dossiers, selected_item)
        if selected_item is None:
            print("[understanding_lab] выход")
            return

        selected_path = selected_item.path.resolve()
        save_state({"last_dossier_path": str(selected_item.path)})

        latest_payload, latest_path, history_path = run_understanding(selected_item)
        print_run_report(selected_item, latest_payload, latest_path, history_path)

        if latest_payload.get("status") != "ok":
            return


def print_recent_dossiers(dossiers: list[DossierItem]) -> None:
    print("\nПоследние dossier-письма:\n")
    for item in dossiers:
        print(
            f"{item.index:>2} | {item.uid:<8} | {item.sent_at:<25} | "
            f"{truncate(item.sender, 28):<28} | {truncate(item.subject, 80)}"
        )


def find_selected_item(dossiers: list[DossierItem], selected_path: Path | None) -> DossierItem | None:
    if selected_path is None:
        return None
    for item in dossiers:
        if item.path.resolve() == selected_path:
            return item
    return None


def choose_item(dossiers: list[DossierItem], selected_item: DossierItem | None) -> DossierItem | None:
    prompt = "\nEnter = повторить последний кейс, номер = выбрать другой кейс, q = выход: "
    choice = input(prompt).strip()
    if choice.lower() in {"q", "quit", "exit", "й"}:
        return None
    if choice == "":
        return selected_item or dossiers[0]
    if not choice.isdigit():
        print("[understanding_lab] нужно Enter, номер из списка или q")
        return choose_item(dossiers, selected_item)

    number = int(choice)
    picked = next((item for item in dossiers if item.index == number), None)
    if picked is None:
        print(f"[understanding_lab] кейс №{number} не найден")
        return choose_item(dossiers, selected_item)
    return picked


def run_understanding(selected_item: DossierItem) -> tuple[dict[str, Any], Path, Path]:
    config_path = resolve_project_path(DEFAULT_CONFIG_PATH)
    run_id = f"understanding-{uuid.uuid4().hex[:8]}"
    context = PipelineContext(run_id=run_id)
    module = LlmUnderstandingModule(dossier_path=str(selected_item.path), config_path=str(config_path))
    result = module.run(context)

    latest_payload = build_latest_payload(
        run_id=run_id,
        dossier_item=selected_item,
        result=result,
        config_path=config_path,
    )
    latest_path, history_path = write_latest_and_history(selected_item.path.parent, latest_payload)
    return latest_payload, latest_path, history_path


def collect_recent_dossiers() -> list[DossierItem]:
    files = sorted(resolve_project_path(DOSSIER_GLOB).parent.glob(resolve_project_path(DOSSIER_GLOB).name))
    if not files:
        files = sorted(resolve_project_path("artifacts/modules/mail_import").glob("run-*/message_*.md"))

    parsed: list[tuple[Path, dict[str, Any]]] = []
    for path in files:
        try:
            payload = load_message_record(path)
            parsed.append((path, payload))
        except Exception:
            continue

    parsed.sort(key=lambda item: str((item[1].get("headers") or {}).get("sent_at", "") or ""), reverse=True)
    recent = parsed[:LIST_LIMIT]
    dossiers: list[DossierItem] = []
    for index, (path, payload) in enumerate(recent, start=1):
        headers = payload.get("headers") or {}
        metadata = payload.get("metadata") or {}
        dossiers.append(
            DossierItem(
                index=index,
                uid=str(metadata.get("uid", "") or payload.get("uid", "unknown")),
                sent_at=str(headers.get("sent_at", "") or ""),
                sender=str(headers.get("sender", "") or ""),
                subject=str(headers.get("subject", "") or ""),
                path=path,
            )
        )
    return dossiers


def build_latest_payload(*, run_id: str, dossier_item: DossierItem, result, config_path: Path) -> dict[str, Any]:
    metrics = result.metrics or {}
    structured_output = metrics.get("structured_output") or {}
    return {
        "run_id": run_id,
        "uid": dossier_item.uid,
        "dossier_path": str(dossier_item.path),
        "backend": metrics.get("backend", ""),
        "model": metrics.get("model", ""),
        "prompt_version": metrics.get("prompt_version", ""),
        "context_version": metrics.get("context_version", ""),
        "status": result.status,
        "error": metrics.get("error", ""),
        "duration_ms": metrics.get("duration_ms", 0),
        "summary": structured_output.get("summary", ""),
        "topic": structured_output.get("topic", ""),
        "customer_need": structured_output.get("customer_need", ""),
        "understanding_note": structured_output.get("understanding_note", ""),
        "response_mode_reason": structured_output.get("response_mode_reason", ""),
        "suggested_next_step": structured_output.get("suggested_next_step", ""),
        "response_mode": structured_output.get("response_mode", ""),
        "confidence": structured_output.get("confidence", ""),
        "structured_output": structured_output,
        "raw_response_text": metrics.get("raw_response_text", ""),
        "prompt_package": metrics.get("prompt_package", {}),
        "config_path": str(config_path),
    }


def write_latest_and_history(target_dir: Path, latest_payload: dict[str, Any]) -> tuple[Path, Path]:
    latest_path = target_dir / "understanding_lab_latest.json"
    history_path = target_dir / "understanding_lab_runs.jsonl"
    latest_path.write_text(json.dumps(latest_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    history_row = {
        "run_id": latest_payload.get("run_id", ""),
        "uid": latest_payload.get("uid", ""),
        "model": latest_payload.get("model", ""),
        "backend": latest_payload.get("backend", ""),
        "prompt_version": latest_payload.get("prompt_version", ""),
        "context_version": latest_payload.get("context_version", ""),
        "status": latest_payload.get("status", ""),
        "error": latest_payload.get("error", ""),
        "duration_ms": latest_payload.get("duration_ms", 0),
        "summary": latest_payload.get("summary", ""),
        "topic": latest_payload.get("topic", ""),
        "customer_need": latest_payload.get("customer_need", ""),
        "understanding_note": latest_payload.get("understanding_note", ""),
        "response_mode_reason": latest_payload.get("response_mode_reason", ""),
        "suggested_next_step": latest_payload.get("suggested_next_step", ""),
        "response_mode": latest_payload.get("response_mode", ""),
        "confidence": latest_payload.get("confidence", ""),
    }
    with history_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(history_row, ensure_ascii=False) + "\n")
    return latest_path, history_path


def print_run_report(
    selected_item: DossierItem,
    latest_payload: dict[str, Any],
    latest_path: Path,
    history_path: Path,
) -> None:
    print(render_console_line(latest_payload))
    print(f"[understanding_lab] summary={single_line(latest_payload.get('summary', ''))}")
    print(f"[understanding_lab] topic={single_line(latest_payload.get('topic', ''))}")
    print(f"[understanding_lab] customer_need={single_line(latest_payload.get('customer_need', ''))}")
    print(f"[understanding_lab] understanding_note={single_line(latest_payload.get('understanding_note', ''))}")
    print(f"[understanding_lab] response_mode_reason={single_line(latest_payload.get('response_mode_reason', ''))}")
    print(f"[understanding_lab] suggested_next_step={single_line(latest_payload.get('suggested_next_step', ''))}")
    print(f"[understanding_lab] case_dir={selected_item.path.parent}")
    print(f"[understanding_lab] latest_json={latest_path}")
    print(f"[understanding_lab] runs_jsonl={history_path}")
    if latest_payload.get("status") != "ok":
        error_text = latest_payload.get("error", "") or "<empty>"
        print(f"[understanding_lab] error={single_line(error_text)}")


def render_console_line(latest_payload: dict[str, Any]) -> str:
    return (
        "[understanding_lab] "
        f"uid={latest_payload.get('uid', '')} "
        f"backend={latest_payload.get('backend', '')} "
        f"model={latest_payload.get('model', '')} "
        f"status={latest_payload.get('status', '')} "
        f"response_mode={latest_payload.get('response_mode', '') or '<empty>'} "
        f"confidence={latest_payload.get('confidence', '') or '<empty>'} "
        f"duration_ms={latest_payload.get('duration_ms', 0)}"
    )


def single_line(value: Any, limit: int = 220) -> str:
    text = str(value or "").replace("\r", " ").replace("\n", " ").strip()
    if not text:
        return "<empty>"
    if len(text) <= limit:
        return text
    return text[: max(limit - 1, 1)] + "…"


def truncate(value: str, limit: int) -> str:
    text = value or ""
    if len(text) <= limit:
        return text
    return text[: max(limit - 1, 1)] + "…"


def load_selected_path_from_state() -> Path | None:
    state = load_state()
    last_path = state.get("last_dossier_path")
    if not last_path:
        return None
    return Path(last_path).resolve()


def load_state() -> dict[str, Any]:
    state_path = resolve_project_path(STATE_PATH)
    if not state_path.exists():
        return {}
    try:
        return json.loads(state_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(payload: dict[str, Any]) -> None:
    state_path = resolve_project_path(STATE_PATH)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
