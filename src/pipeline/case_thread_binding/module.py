from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from email.utils import parseaddr
from pathlib import Path
from uuid import uuid4

from src.layers.state.case_thread_registry_store import CaseThreadRegistryStore
from src.shared.common.message_dossier import load_message_record, resolve_dossier_path, write_message_dossier
from src.shared.contracts.module_contract import ModuleResult
from src.shared.models.entities import Case, Thread
from src.shared.models.pipeline_context import PipelineContext


class CaseThreadBindingModule:
    name = "case_thread_binding"

    def __init__(
        self,
        parsed_email_path: str,
        artifacts_dir: str = "artifacts",
        subject_sender_fallback_lookback_days: int = 14,
    ) -> None:
        self.parsed_email_path = parsed_email_path
        self.registry_store = CaseThreadRegistryStore(base_dir=artifacts_dir)
        self.subject_sender_fallback_lookback_days = subject_sender_fallback_lookback_days

    def run(self, context: PipelineContext) -> ModuleResult:
        parsed_path = Path(self.parsed_email_path)
        if not parsed_path.exists():
            return ModuleResult(context=context, status="error", notes=[f"parsed_email missing: {parsed_path}"])

        try:
            parsed_email = load_message_record(parsed_path)
        except Exception as exc:
            return ModuleResult(context=context, status="error", notes=[f"message record unreadable: {exc}"])

        if not isinstance(parsed_email, dict):
            return ModuleResult(context=context, status="error", notes=["message record must be an object"])

        message_id = str(parsed_email.get("message_id", "") or "").strip()
        if not message_id:
            return ModuleResult(context=context, status="error", notes=["parsed_email missing message_id"])
        if message_id.startswith("__bootstrap_cursor__"):
            return ModuleResult(context=context, status="skipped", notes=["bootstrap cursor message skipped"])

        headers = parsed_email.get("headers") or {}
        if not isinstance(headers, dict):
            headers = {}

        uid = self._resolve_uid(parsed_email, parsed_path)
        dossier_path = resolve_dossier_path(parsed_path, uid)
        direction = str(parsed_email.get("direction", "") or "inbound").strip() or "inbound"
        sender = self._extract_sender(headers)
        sender_normalized = self._normalize_sender(sender)
        subject = str(headers.get("subject", "") or "").strip()
        subject_normalized = self._normalize_subject(subject)
        sent_at_raw = str(headers.get("sent_at", "") or "").strip()
        sent_at_dt = self._parse_dt(sent_at_raw)
        in_reply_to = str(headers.get("in_reply_to", "") or "").strip()
        references = self._normalize_references(headers.get("references"))
        references_joined = " | ".join(references)
        metadata = parsed_email.get("metadata") or {}
        if not isinstance(metadata, dict):
            metadata = {}

        source_mode = str(metadata.get("source_mode", "") or "").strip()
        mailbox = str(metadata.get("mailbox", "") or "").strip()
        raw_path = str(parsed_email.get("raw_path", "") or "").strip()

        all_rows = self.registry_store.read_all()
        existing_row = self.registry_store.find_by_message_id(message_id)
        current_run_status = ""

        if existing_row is not None:
            row = existing_row
            created = False
            row_number = self._find_row_number(all_rows, message_id)
            current_run_status = "duplicate_message"
        else:
            resolution = self._resolve_binding(
                rows=all_rows,
                sender_normalized=sender_normalized,
                subject_normalized=subject_normalized,
                sent_at_dt=sent_at_dt,
                in_reply_to=in_reply_to,
                references=references,
            )

            if resolution is None:
                case_id = self.registry_store.next_case_id(all_rows)
                thread_id = self.registry_store.next_thread_id(all_rows)
                binding_rule = "new_case_thread"
                matched_message_id = ""
                registry_status = "new_case_thread"
            else:
                case_id = resolution["case_id"]
                thread_id = resolution["thread_id"]
                binding_rule = resolution["binding_rule"]
                matched_message_id = resolution["matched_message_id"]
                registry_status = "bound_existing_thread"

            record = self.registry_store.build_record(
                binding_id=f"bind_{uuid4().hex[:12]}",
                message_id=message_id,
                direction=direction,
                sender=sender,
                sender_normalized=sender_normalized,
                subject=subject,
                subject_normalized=subject_normalized,
                sent_at=sent_at_raw,
                in_reply_to=in_reply_to,
                references=references_joined,
                source_mode=source_mode,
                uid=uid,
                mailbox=mailbox,
                raw_path=raw_path,
                parsed_email_path=str(parsed_path),
                case_id=case_id,
                thread_id=thread_id,
                binding_rule=binding_rule,
                matched_message_id=matched_message_id,
                status=registry_status,
            )
            row, created, row_number = self.registry_store.append_or_get_existing(record)
            all_rows = self.registry_store.read_all()
            current_run_status = str(row.get("status", "") or "ok") if created else "duplicate_message"

        case_id = str(row.get("case_id", "") or "")
        thread_id = str(row.get("thread_id", "") or "")
        binding_rule = str(row.get("binding_rule", "") or "")
        matched_message_id = str(row.get("matched_message_id", "") or "")
        status = current_run_status or str(row.get("status", "") or "ok")

        thread_rows = self._sorted_thread_rows(all_rows, thread_id)
        thread_message_ids = [str(item.get("message_id", "") or "") for item in thread_rows if item.get("message_id")]

        context.thread = Thread(thread_id=thread_id, message_ids=thread_message_ids)
        context.case = Case(case_id=case_id, thread_id=thread_id, status="open", history=thread_message_ids)

        binding_payload = {
            "uid": uid,
            "message_id": message_id,
            "direction": direction,
            "sender": sender,
            "subject": subject,
            "case_id": case_id,
            "thread_id": thread_id,
            "binding_rule": binding_rule,
            "matched_message_id": matched_message_id,
            "status": status,
            "registry_path": str(self.registry_store.registry_path),
            "registry_row_number": row_number,
            "created": created,
            "message_chain_headers": {
                "in_reply_to": in_reply_to,
                "references": references,
            },
            "thread_history": [
                {
                    "message_id": str(item.get("message_id", "") or ""),
                    "direction": str(item.get("direction", "") or ""),
                    "sender": str(item.get("sender", "") or ""),
                    "subject": str(item.get("subject", "") or ""),
                    "sent_at": str(item.get("sent_at", "") or ""),
                    "binding_rule": str(item.get("binding_rule", "") or ""),
                    "status": str(item.get("status", "") or ""),
                    "parsed_email_path": str(item.get("parsed_email_path", "") or ""),
                }
                for item in thread_rows
            ],
        }

        parsed_email.setdefault("modules", {})[self.name] = binding_payload
        write_message_dossier(dossier_path, parsed_email)

        context.enrichment[self.name] = binding_payload
        context.artifacts.setdefault(self.name, []).append(str(dossier_path))

        metrics = {
            "uid": uid,
            "message_id": message_id,
            "case_id": case_id,
            "thread_id": thread_id,
            "binding_rule": binding_rule,
            "matched_message_id": matched_message_id,
            "status": status,
            "created": created,
            "registry_path": str(self.registry_store.registry_path),
            "registry_row_number": row_number,
            "thread_messages_count": len(thread_rows),
            "binding_path": str(dossier_path),
            "dossier_path": str(dossier_path),
        }
        notes = [
            f"case_thread_binding processed uid={uid}",
            f"status={status}",
            f"case_id={case_id}",
            f"thread_id={thread_id}",
            f"binding_rule={binding_rule or '<empty>'}",
        ]
        if matched_message_id:
            notes.append(f"matched_message_id={matched_message_id}")

        return ModuleResult(
            context=context,
            status="ok",
            notes=notes,
            artifact_refs=[str(dossier_path)],
            metrics=metrics,
        )

    def _resolve_binding(
        self,
        *,
        rows: list[dict[str, str]],
        sender_normalized: str,
        subject_normalized: str,
        sent_at_dt: datetime | None,
        in_reply_to: str,
        references: list[str],
    ) -> dict[str, str] | None:
        by_message_id = {
            str(row.get("message_id", "") or "").strip(): row
            for row in rows
            if str(row.get("message_id", "") or "").strip()
        }

        if in_reply_to and in_reply_to in by_message_id:
            matched = by_message_id[in_reply_to]
            return {
                "case_id": str(matched.get("case_id", "") or ""),
                "thread_id": str(matched.get("thread_id", "") or ""),
                "binding_rule": "in_reply_to_exact",
                "matched_message_id": in_reply_to,
            }

        for ref in reversed(references):
            if ref and ref in by_message_id:
                matched = by_message_id[ref]
                return {
                    "case_id": str(matched.get("case_id", "") or ""),
                    "thread_id": str(matched.get("thread_id", "") or ""),
                    "binding_rule": "references_exact",
                    "matched_message_id": ref,
                }

        fallback_match = self._resolve_subject_sender_fallback(
            rows=rows,
            sender_normalized=sender_normalized,
            subject_normalized=subject_normalized,
            sent_at_dt=sent_at_dt,
        )
        if fallback_match is not None:
            return fallback_match

        return None

    def _resolve_subject_sender_fallback(
        self,
        *,
        rows: list[dict[str, str]],
        sender_normalized: str,
        subject_normalized: str,
        sent_at_dt: datetime | None,
    ) -> dict[str, str] | None:
        if not sender_normalized or not subject_normalized:
            return None

        candidates: list[dict[str, str]] = []
        for row in rows:
            if str(row.get("sender_normalized", "") or "") != sender_normalized:
                continue
            if str(row.get("subject_normalized", "") or "") != subject_normalized:
                continue

            row_dt = self._parse_dt(str(row.get("sent_at", "") or ""))
            if sent_at_dt is not None and row_dt is not None:
                if row_dt > sent_at_dt:
                    continue
                if sent_at_dt - row_dt > timedelta(days=self.subject_sender_fallback_lookback_days):
                    continue
            candidates.append(row)

        if not candidates:
            return None

        unique_threads = {str(row.get("thread_id", "") or "") for row in candidates if row.get("thread_id")}
        if len(unique_threads) != 1:
            return None

        candidates.sort(key=self._row_sort_key, reverse=True)
        matched = candidates[0]
        return {
            "case_id": str(matched.get("case_id", "") or ""),
            "thread_id": str(matched.get("thread_id", "") or ""),
            "binding_rule": "sender_subject_fallback_unique",
            "matched_message_id": str(matched.get("message_id", "") or ""),
        }

    @staticmethod
    def _extract_sender(headers: dict) -> str:
        sender_raw = str(headers.get("sender", "") or "").strip()
        parsed_email = parseaddr(sender_raw)[1].strip()
        return parsed_email or sender_raw

    @staticmethod
    def _normalize_sender(sender: str) -> str:
        parsed_email = parseaddr(str(sender or ""))[1].strip().lower()
        if parsed_email:
            return parsed_email
        return str(sender or "").strip().lower()

    @staticmethod
    def _normalize_subject(subject: str) -> str:
        value = " ".join(str(subject or "").split()).strip().lower()
        while True:
            updated = re.sub(r"^(?:re|fw|fwd)\s*:\s*", "", value, flags=re.IGNORECASE).strip()
            if updated == value:
                break
            value = updated
        return value

    @staticmethod
    def _normalize_references(value) -> list[str]:
        if isinstance(value, list):
            result = []
            for item in value:
                text = str(item or "").strip()
                if text:
                    result.append(text)
            return result
        if isinstance(value, str):
            return [part.strip() for part in value.split() if part.strip()]
        return []

    @staticmethod
    def _resolve_uid(parsed_email: dict, parsed_path: Path) -> str:
        metadata = parsed_email.get("metadata") or {}
        if isinstance(metadata, dict):
            raw_uid = str(metadata.get("uid", "") or "").strip()
            if raw_uid:
                return raw_uid
        match = re.search(r"(?:parsed_email|message)_(.+)\.(?:json|md)$", parsed_path.name)
        if match:
            return match.group(1)
        return "unknown"

    @staticmethod
    def _parse_dt(raw_value: str) -> datetime | None:
        text = str(raw_value or "").strip()
        if not text:
            return None

        candidates = [text]
        if "T" not in text and " " in text:
            candidates.append(text.replace(" ", "T", 1))
        if text.endswith("Z"):
            candidates.append(text[:-1] + "+00:00")

        for candidate in candidates:
            try:
                dt = datetime.fromisoformat(candidate)
                if dt.tzinfo is None:
                    return dt.replace(tzinfo=timezone.utc)
                return dt
            except Exception:
                continue
        return None

    def _sorted_thread_rows(self, rows: list[dict[str, str]], thread_id: str) -> list[dict[str, str]]:
        thread_rows = [row for row in rows if str(row.get("thread_id", "") or "") == thread_id]
        thread_rows.sort(key=self._row_sort_key)
        return thread_rows

    def _find_row_number(self, rows: list[dict[str, str]], message_id: str) -> int:
        for idx, row in enumerate(rows, start=2):
            if str(row.get("message_id", "") or "") == message_id:
                return idx
        return 0

    def _row_sort_key(self, row: dict[str, str]):
        sent_at = self._parse_dt(str(row.get("sent_at", "") or ""))
        created_at = self._parse_dt(str(row.get("created_at", "") or ""))
        return sent_at or created_at or datetime(1970, 1, 1, tzinfo=timezone.utc)
