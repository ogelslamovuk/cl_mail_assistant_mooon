from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

PAYLOAD_START = "<!-- MESSAGE_DOSSIER_PAYLOAD_START -->"
PAYLOAD_END = "<!-- MESSAGE_DOSSIER_PAYLOAD_END -->"


def load_message_record(path: str | Path) -> dict[str, Any]:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Message record file not found: {file_path}")

    suffix = file_path.suffix.lower()
    if suffix == ".json":
        payload = json.loads(file_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("JSON message record must be an object")
        return payload

    text = file_path.read_text(encoding="utf-8")
    match = re.search(
        rf"{re.escape(PAYLOAD_START)}\n(.*?)\n{re.escape(PAYLOAD_END)}",
        text,
        flags=re.DOTALL,
    )
    if not match:
        raise ValueError(f"Machine payload markers not found in dossier: {file_path}")

    payload = json.loads(match.group(1))
    if not isinstance(payload, dict):
        raise ValueError("Dossier machine payload must be an object")
    return payload


def resolve_dossier_path(message_record_path: str | Path, uid: str) -> Path:
    path = Path(message_record_path)
    if path.suffix.lower() in {".md", ".txt"}:
        return path
    return path.with_name(f"message_{uid}.md")


def write_message_dossier(path: str | Path, payload: dict[str, Any]) -> str:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_render_dossier(payload), encoding="utf-8")
    return str(target)


def _render_dossier(payload: dict[str, Any]) -> str:
    headers = payload.get("headers") or {}
    metadata = payload.get("metadata") or {}
    modules = payload.get("modules") or {}
    attachment = modules.get("attachment_extraction") or {}
    enrich = modules.get("identity_context_enrichment") or {}
    binding = modules.get("case_thread_binding") or {}
    llm_understanding = modules.get("llm_understanding") or {}

    uid = _resolve_uid(payload)
    message_id = str(payload.get("message_id", "") or "")
    sender = str(headers.get("sender", "") or "")
    subject = str(headers.get("subject", "") or "")
    sent_at = str(headers.get("sent_at", "") or "")
    direction = str(payload.get("direction", "") or "")
    raw_path = str(payload.get("raw_path", "") or "")
    body_text = str(payload.get("body_text", "") or "")
    preferred_body_source = str(payload.get("preferred_body_source", "") or "")

    attachment_items = attachment.get("items") or []
    attachments_count = len(attachment_items)
    attachments_with_text = sum(1 for item in attachment_items if bool(item.get("text_found")))

    enrich_result = enrich.get("result") or {}
    ticket_db_status = str(enrich_result.get("providers", {}).get("ticket_db", {}).get("status", "") or "")
    selected_lookup_email = str(enrich_result.get("selected_lookup_email", "") or "")
    resolved_match = enrich_result.get("resolved_match") or {}
    resolved_ticket = str(resolved_match.get("ticket", "") or "")

    case_id = str(binding.get("case_id", "") or "")
    thread_id = str(binding.get("thread_id", "") or "")
    binding_rule = str(binding.get("binding_rule", "") or "")
    binding_status = str(binding.get("status", "") or "")

    llm_status = str(llm_understanding.get("status", "") or "")
    llm_backend = str(llm_understanding.get("backend", "") or "")
    llm_model = str(llm_understanding.get("model", "") or "")
    llm_prompt_version = str(llm_understanding.get("prompt_version", "") or "")
    llm_context_version = str(llm_understanding.get("context_version", "") or "")
    llm_duration_ms = llm_understanding.get("duration_ms", "")
    llm_error = str(llm_understanding.get("error", "") or "")
    llm_output = llm_understanding.get("structured_output") or {}
    if not isinstance(llm_output, dict):
        llm_output = {}

    lines: list[str] = []
    lines.append(f"# Message dossier {uid}")
    lines.append("")
    lines.append(f"- UID: {uid}")
    lines.append(f"- Message-ID: {message_id or '<empty>'}")
    lines.append(f"- Direction: {direction or '<empty>'}")
    lines.append(f"- From: {sender or '<empty>'}")
    lines.append(f"- Subject: {subject or '<empty>'}")
    lines.append(f"- Sent at: {sent_at or '<empty>'}")
    lines.append(f"- Preferred body source: {preferred_body_source or '<empty>'}")
    lines.append(f"- Raw email: {raw_path or '<empty>'}")
    lines.append("")

    lines.append("## Case / Thread")
    lines.append("")
    lines.append(f"- Case ID: {case_id or '<empty>'}")
    lines.append(f"- Thread ID: {thread_id or '<empty>'}")
    lines.append(f"- Binding rule: {binding_rule or '<empty>'}")
    lines.append(f"- Binding status: {binding_status or '<empty>'}")
    lines.append("")

    lines.append("## Enrichment")
    lines.append("")
    lines.append(f"- Ticket DB status: {ticket_db_status or '<empty>'}")
    lines.append(f"- Selected lookup email: {selected_lookup_email or '<empty>'}")
    lines.append(f"- Resolved ticket: {resolved_ticket or '<empty>'}")
    lines.append("")

    lines.append("## Attachments")
    lines.append("")
    lines.append(f"- Count: {attachments_count}")
    lines.append(f"- Text found in: {attachments_with_text}")
    if attachment_items:
        lines.append("")
        for item in attachment_items:
            lines.append(f"- {str(item.get('filename_saved') or item.get('filename_original') or '<empty>')}")
            lines.append(f"  - content_type: {str(item.get('content_type', '') or '<empty>')}")
            lines.append(f"  - text_found: {'yes' if bool(item.get('text_found')) else 'no'}")
            preview = str(item.get("text_preview", "") or "")
            if preview:
                lines.append(f"  - preview: {preview}")
    lines.append("")

    if llm_understanding:
        lines.append("## LLM Understanding")
        lines.append("")
        lines.append(f"- Status: {llm_status or '<empty>'}")
        lines.append(f"- Response mode: {str(llm_output.get('response_mode', '') or '<empty>')}")
        lines.append(f"- Confidence: {str(llm_output.get('confidence', '') or '<empty>')}")
        lines.append(f"- Topic: {str(llm_output.get('topic', '') or '<empty>')}")
        lines.append(f"- Customer need: {str(llm_output.get('customer_need', '') or '<empty>')}")
        lines.append(f"- Summary: {str(llm_output.get('summary', '') or '<empty>')}")
        understanding_note = str(llm_output.get('understanding_note', '') or '').strip()
        response_mode_reason = str(llm_output.get('response_mode_reason', '') or '').strip()
        suggested_next_step = str(llm_output.get('suggested_next_step', '') or '').strip()
        if understanding_note:
            lines.append(f"- Understanding note: {understanding_note}")
        if response_mode_reason:
            lines.append(f"- Response mode reason: {response_mode_reason}")
        if suggested_next_step:
            lines.append(f"- Suggested next step: {suggested_next_step}")
        if llm_backend or llm_model:
            lines.append(f"- Backend/model: {(llm_backend or '<empty>')}/{(llm_model or '<empty>')}")
        if llm_prompt_version or llm_context_version:
            lines.append(f"- Prompt/context version: {(llm_prompt_version or '<empty>')}/{(llm_context_version or '<empty>')}")
        if llm_duration_ms != "":
            lines.append(f"- Duration ms: {llm_duration_ms}")
        if llm_error:
            lines.append(f"- Error: {llm_error}")
        entities = llm_output.get('entities') or []
        if entities:
            lines.append("")
            lines.append("Entities:")
            for entity in entities:
                if not isinstance(entity, dict):
                    continue
                entity_type = str(entity.get('type', '') or '<empty>')
                entity_value = str(entity.get('value', '') or '<empty>')
                lines.append(f"- {entity_type}: {entity_value}")
        lines.append("")

    lines.append("## Body")
    lines.append("")
    lines.append("```")
    lines.append(body_text.rstrip())
    lines.append("```")
    lines.append("")

    lines.append(PAYLOAD_START)
    lines.append(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
    lines.append(PAYLOAD_END)
    lines.append("")

    return "\n".join(lines)


def _resolve_uid(payload: dict[str, Any]) -> str:
    metadata = payload.get("metadata") or {}
    if isinstance(metadata, dict):
        uid = str(metadata.get("uid", "") or "").strip()
        if uid:
            return uid
        fixture_ref = str(metadata.get("fixture_ref", "") or "").strip()
        if fixture_ref:
            return fixture_ref
    return str(payload.get("uid", "") or "unknown")
