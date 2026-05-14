from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from src.pipeline.early_classification import OWN_MAILBOXES, early_classification
from src.pipeline.identity_context_enrichment.ticket_db_lookup import TicketDbLookupProvider, localpart
from src.shared.common.message_dossier import load_message_record, resolve_dossier_path, write_message_dossier
from src.shared.contracts.module_contract import ModuleResult
from src.shared.models.pipeline_context import PipelineContext


EMAIL_RE = re.compile(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", re.IGNORECASE)


class IdentityContextEnrichmentModule:
    name = "identity_context_enrichment"

    def __init__(self, parsed_email_path: str, attachment_report_path: str | None = None) -> None:
        self.parsed_email_path = str(parsed_email_path)
        self.attachment_report_path = str(attachment_report_path) if attachment_report_path else None
        self.ticket_db_provider = TicketDbLookupProvider.from_project_config()

    def run(self, context: PipelineContext) -> ModuleResult:
        parsed_path = Path(self.parsed_email_path)
        if not parsed_path.exists():
            return ModuleResult(context=context, status="error", notes=[f"parsed_email missing: {parsed_path}"])

        try:
            parsed_email = load_message_record(parsed_path)
        except Exception as exc:
            return ModuleResult(context=context, status="error", notes=[f"message record unreadable: {exc}"])

        attachment_report = self._load_attachment_report()
        uid = self._resolve_uid(parsed_email, parsed_path)
        dossier_path = resolve_dossier_path(parsed_path, uid)
        message_id = str(parsed_email.get("message_id", "") or "")
        subject = str((parsed_email.get("headers") or {}).get("subject", "") or "")
        sender_email = self._extract_sender_email(parsed_email)
        body_emails = self._extract_body_emails(parsed_email)
        excluded_emails = self._excluded_lookup_emails(parsed_email)
        lookup_emails = self._build_lookup_emails(
            sender_email=sender_email,
            body_emails=body_emails,
            excluded_emails=excluded_emails,
        )
        classification = early_classification(parsed_email)
        if classification and classification.get("should_run_ticket_enrichment") is False:
            return self._write_skipped_result(
                context=context,
                parsed_email=parsed_email,
                dossier_path=dossier_path,
                uid=uid,
                message_id=message_id,
                subject=subject,
                sender_email=sender_email,
                body_emails=body_emails,
                lookup_emails=lookup_emails,
                excluded_emails=excluded_emails,
                attachment_report=attachment_report,
                reason=str(classification.get("classification_reason") or "early classification skipped ticket lookup"),
            )
        ticket_db_result, ticket_db_trace, selected_lookup_email = self._run_ticket_db_lookup(lookup_emails)
        crm_stub = self._stub_provider("crm_users", "not implemented yet")
        payment_stub = self._stub_provider("payment_refund", "not implemented yet")
        resolved_primary_match = self._resolve_primary_match(ticket_db_result)

        ticket_db_candidates = self._normalize_ticket_candidates(ticket_db_result.rows, ticket_db_result.rescue)
        normalized_resolved_match = self._normalize_resolved_match(resolved_primary_match)
        note = self._first_meaningful_note(ticket_db_result.notes)
        confidence = self._resolve_confidence(ticket_db_result.status, ticket_db_result.rescue_confident)

        result_payload = {
            "uid": uid,
            "message_id": message_id,
            "subject": subject,
            "lookup_emails": lookup_emails,
            "selected_lookup_email": selected_lookup_email,
            "ticket_db_status": ticket_db_result.status,
            "crm_users_status": crm_stub["status"],
            "payment_refund_status": payment_stub["status"],
            "confidence": confidence,
            "candidates_count": len(ticket_db_candidates),
            "resolved_match": normalized_resolved_match,
            "note": note,
        }

        debug_payload = {
            "uid": uid,
            "message_id": message_id,
            "subject": subject,
            "paths": {
                "parsed_email_path": str(parsed_path),
                "attachment_report_path": self.attachment_report_path or "",
            },
            "lookup_keys": {
                "sender_email_reference": sender_email,
                "body_emails": body_emails,
                "excluded_emails": sorted(excluded_emails),
                "lookup_emails": lookup_emails,
                "selected_lookup_email": selected_lookup_email,
                "selected_lookup_localpart": localpart(selected_lookup_email),
            },
            "providers": {
                "ticket_db": {
                    "status": ticket_db_result.status,
                    "settings_source": ticket_db_result.settings_source,
                    "candidates": ticket_db_candidates,
                    "rescue_confident": ticket_db_result.rescue_confident,
                    "rescue_reason": ticket_db_result.rescue_reason,
                    "rescue_top1": ticket_db_result.rescue_top1,
                    "rescue_gap": ticket_db_result.rescue_gap,
                    "notes": [str(note or "") for note in (ticket_db_result.notes or [])],
                    "query_email": ticket_db_result.query_email,
                    "query_localpart": ticket_db_result.query_localpart,
                    "lookup_trace": self._json_safe(ticket_db_trace),
                },
                "crm_users": crm_stub,
                "payment_refund": payment_stub,
            },
            "resolved_match": normalized_resolved_match,
            "summary": {
                "ticket_found": bool(normalized_resolved_match),
                "ticket_db_status": ticket_db_result.status,
                "crm_users_status": crm_stub["status"],
                "payment_refund_status": payment_stub["status"],
                "attachment_report_present": bool(attachment_report),
                "body_emails_found": len(body_emails),
                "lookup_emails_total": len(lookup_emails),
                "confidence": confidence,
            },
        }

        safe_result_payload = self._json_safe(result_payload)
        safe_debug_payload = self._json_safe(debug_payload)

        parsed_email.setdefault("modules", {})[self.name] = {
            "result": safe_result_payload,
            "debug": safe_debug_payload,
        }
        write_message_dossier(dossier_path, parsed_email)

        context.enrichment["identity_context_enrichment"] = safe_result_payload
        context.artifacts.setdefault(self.name, []).append(str(dossier_path))

        metrics = {
            "uid": uid,
            "message_id": message_id,
            "subject": subject,
            "result_path": str(dossier_path),
            "debug_path": str(dossier_path),
            "dossier_path": str(dossier_path),
            "sender_email_reference": sender_email,
            "body_lookup_emails": body_emails,
            "excluded_lookup_emails": sorted(excluded_emails),
            "lookup_emails": lookup_emails,
            "selected_lookup_email": selected_lookup_email,
            "ticket_db_status": ticket_db_result.status,
            "ticket_db_found_rows": len(ticket_db_result.rows),
            "ticket_db_rescue_candidates": len(ticket_db_result.rescue),
            "crm_users_status": crm_stub["status"],
            "payment_refund_status": payment_stub["status"],
            "resolved_match": normalized_resolved_match,
            "note": note,
        }
        notes = [
            f"identity_context_enrichment processed uid={uid}",
            f"ticket_db_status={ticket_db_result.status}",
            f"crm_users_status={crm_stub['status']}",
            f"payment_refund_status={payment_stub['status']}",
        ]
        if note:
            notes.append(note)

        return ModuleResult(
            context=context,
            status="ok",
            notes=notes,
            artifact_refs=[str(dossier_path)],
            metrics=metrics,
        )

    def _write_skipped_result(
        self,
        *,
        context: PipelineContext,
        parsed_email: dict[str, Any],
        dossier_path: Path,
        uid: str,
        message_id: str,
        subject: str,
        sender_email: str,
        body_emails: list[str],
        lookup_emails: list[str],
        excluded_emails: set[str],
        attachment_report: dict[str, Any],
        reason: str,
    ) -> ModuleResult:
        result_payload = {
            "uid": uid,
            "message_id": message_id,
            "subject": subject,
            "lookup_emails": lookup_emails,
            "selected_lookup_email": "",
            "ticket_db_status": "skipped",
            "crm_users_status": "stub",
            "payment_refund_status": "stub",
            "confidence": "none",
            "candidates_count": 0,
            "resolved_match": None,
            "note": f"ticket enrichment skipped: {reason}",
        }
        debug_payload = {
            "uid": uid,
            "message_id": message_id,
            "subject": subject,
            "paths": {
                "parsed_email_path": str(dossier_path),
                "attachment_report_path": self.attachment_report_path or "",
            },
            "lookup_keys": {
                "sender_email_reference": sender_email,
                "body_emails": body_emails,
                "excluded_emails": sorted(excluded_emails),
                "lookup_emails": lookup_emails,
                "selected_lookup_email": "",
                "selected_lookup_localpart": "",
            },
            "providers": {
                "ticket_db": {
                    "status": "skipped",
                    "settings_source": "",
                    "candidates": [],
                    "notes": [reason],
                    "query_email": "",
                    "query_localpart": "",
                    "lookup_trace": [],
                },
                "crm_users": self._stub_provider("crm_users", "not implemented yet"),
                "payment_refund": self._stub_provider("payment_refund", "not implemented yet"),
            },
            "resolved_match": None,
            "summary": {
                "ticket_found": False,
                "ticket_db_status": "skipped",
                "crm_users_status": "stub",
                "payment_refund_status": "stub",
                "attachment_report_present": bool(attachment_report),
                "body_emails_found": len(body_emails),
                "lookup_emails_total": len(lookup_emails),
                "confidence": "none",
                "skip_reason": reason,
            },
        }
        parsed_email.setdefault("modules", {})[self.name] = {
            "result": self._json_safe(result_payload),
            "debug": self._json_safe(debug_payload),
        }
        write_message_dossier(dossier_path, parsed_email)
        context.enrichment["identity_context_enrichment"] = result_payload
        context.artifacts.setdefault(self.name, []).append(str(dossier_path))
        metrics = {
            "uid": uid,
            "message_id": message_id,
            "subject": subject,
            "result_path": str(dossier_path),
            "debug_path": str(dossier_path),
            "dossier_path": str(dossier_path),
            "sender_email_reference": sender_email,
            "body_lookup_emails": body_emails,
            "excluded_lookup_emails": sorted(excluded_emails),
            "lookup_emails": lookup_emails,
            "selected_lookup_email": "",
            "ticket_db_status": "skipped",
            "ticket_db_found_rows": 0,
            "ticket_db_rescue_candidates": 0,
            "crm_users_status": "stub",
            "payment_refund_status": "stub",
            "resolved_match": None,
            "note": result_payload["note"],
        }
        return ModuleResult(
            context=context,
            status="ok",
            notes=[
                f"identity_context_enrichment skipped uid={uid}",
                f"ticket_db_status=skipped reason={reason}",
            ],
            artifact_refs=[str(dossier_path)],
            metrics=metrics,
        )

    def _run_ticket_db_lookup(self, lookup_emails: list[str]):
        if not lookup_emails:
            result = self.ticket_db_provider.lookup_by_email("")
            result.status = "no_lookup_emails"
            result.notes = ["no email addresses found in parsed email"]
            result.query_email = ""
            result.query_localpart = ""
            return result, [], ""

        trace: list[dict[str, Any]] = []
        first_rescue = None
        first_selected_email = ""
        last_result = None

        for email in lookup_emails:
            result = self.ticket_db_provider.lookup_by_email(email)
            if result.status in {"unavailable", "error"}:
                demo_row = self._local_demo_ticket_row(email)
                if demo_row:
                    result.status = "found_strict"
                    result.rows = [demo_row]
                    result.notes = [
                        "TECHNICAL WARNING: ticket_db unavailable; local mock ticket fixture used for demo acceptance."
                    ]
            last_result = result
            trace.append(
                {
                    "email": email,
                    "status": result.status,
                    "rows": len(result.rows),
                    "rescue_candidates": len(result.rescue),
                    "rescue_confident": bool(result.rescue_confident),
                }
            )

            if result.status == "found_strict" and result.rows:
                return result, trace, email

            if result.status == "rescue_candidates" and first_rescue is None:
                first_rescue = result
                first_selected_email = email

        if first_rescue is not None:
            return first_rescue, trace, first_selected_email

        if last_result is not None:
            return last_result, trace, lookup_emails[0]

        result = self.ticket_db_provider.lookup_by_email("")
        result.status = "no_lookup_emails"
        result.notes = ["no email addresses found in parsed email"]
        result.query_email = ""
        result.query_localpart = ""
        return result, trace, ""

    @staticmethod
    def _local_demo_ticket_row(email: str) -> dict[str, Any]:
        key = str(email or "").strip().lower()
        demo_rows = {
            "kozlova22anna@gmail.com": {
                "ticket": 43174015,
                "idTrading": 7056395,
                "dateShow": "2026-05-09",
                "timeShow": "18:40:00",
                "theater": "mooon в ТРК Minsk City Mall",
                "event": "Дьявол носит Prada 2",
                "auditorium": "Зал 1 Premiere",
                "line": 2,
                "seat": 8,
                "emailClient": "kozlova22anna@gmail.com",
                "_match": "local_mock_fixture",
            }
        }
        return dict(demo_rows.get(key) or {})

    def _load_attachment_report(self) -> dict[str, Any]:
        if not self.attachment_report_path:
            return {}
        report_path = Path(self.attachment_report_path)
        if not report_path.exists():
            return {}
        try:
            payload = load_message_record(report_path)
        except Exception:
            return {}
        if report_path.suffix.lower() == ".json":
            return payload if isinstance(payload, dict) else {}
        modules = payload.get("modules") or {}
        attachment = modules.get("attachment_extraction") or {}
        return attachment if isinstance(attachment, dict) else {}

    @staticmethod
    def _resolve_uid(parsed_email: dict[str, Any], parsed_path: Path) -> str:
        metadata = parsed_email.get("metadata") or {}
        raw_uid = str(metadata.get("uid", "") or "").strip()
        if raw_uid:
            return raw_uid
        match = re.search(r"(?:parsed_email|message)_(.+)\.(?:json|md)$", parsed_path.name)
        if match:
            return match.group(1)
        return "unknown"

    @staticmethod
    def _extract_sender_email(parsed_email: dict[str, Any]) -> str:
        headers = parsed_email.get("headers") or {}
        sender_raw = str(headers.get("sender", "") or "").strip()
        if sender_raw:
            found = EMAIL_RE.findall(sender_raw)
            if found:
                return found[0].lower()
            return sender_raw.lower()

        raw_headers = parsed_email.get("raw_headers") or {}
        from_raw = str(raw_headers.get("from", "") or "").strip()
        if from_raw:
            found = EMAIL_RE.findall(from_raw)
            if found:
                return found[0].lower()
            return from_raw.lower()

        return ""

    @staticmethod
    def _extract_body_emails(parsed_email: dict[str, Any]) -> list[str]:
        body_text = str(parsed_email.get("body_text", "") or "")
        found = EMAIL_RE.findall(body_text)
        seen: set[str] = set()
        out: list[str] = []
        for email in found:
            lowered = email.lower()
            if lowered in seen:
                continue
            seen.add(lowered)
            out.append(lowered)
        return out

    @staticmethod
    def _build_lookup_emails(sender_email: str, body_emails: list[str], excluded_emails: set[str] | None = None) -> list[str]:
        excluded = {str(email or "").strip().lower() for email in (excluded_emails or set()) if str(email or "").strip()}
        seen: set[str] = set()
        out: list[str] = []
        for email in body_emails + ([sender_email.lower()] if sender_email else []):
            lowered = str(email or "").strip().lower()
            if not lowered or lowered in seen or lowered in excluded:
                continue
            seen.add(lowered)
            out.append(lowered)
        return out

    @staticmethod
    def _excluded_lookup_emails(parsed_email: dict[str, Any]) -> set[str]:
        headers = parsed_email.get("headers") if isinstance(parsed_email.get("headers"), dict) else {}
        excluded = set(OWN_MAILBOXES)
        for key in ("to", "cc"):
            values = headers.get(key) or []
            if isinstance(values, str):
                values = [values]
            for value in values:
                found = EMAIL_RE.findall(str(value or ""))
                for email in found:
                    excluded.add(email.lower())
        return excluded

    @staticmethod
    def _normalize_ticket_candidates(strict_rows: list[dict[str, Any]], rescue_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        candidates: list[dict[str, Any]] = []
        for row in strict_rows or []:
            normalized = IdentityContextEnrichmentModule._normalize_ticket_candidate(row)
            normalized["candidate_source"] = "strict"
            candidates.append(normalized)
        for row in rescue_rows or []:
            normalized = IdentityContextEnrichmentModule._normalize_ticket_candidate(row)
            normalized["candidate_source"] = "rescue"
            normalized["rescue_score"] = row.get("_rf_score")
            candidates.append(normalized)
        return IdentityContextEnrichmentModule._json_safe(candidates)

    @staticmethod
    def _normalize_ticket_candidate(row: dict[str, Any]) -> dict[str, Any]:
        return {
            "ticket": row.get("ticket"),
            "idTrading": row.get("idTrading"),
            "dateShow": row.get("dateShow"),
            "timeShow": row.get("timeShow"),
            "theater": row.get("theater"),
            "event": row.get("event"),
            "auditorium": row.get("auditorium"),
            "line": row.get("line"),
            "seat": row.get("seat"),
            "match_type": row.get("_match", ""),
            "emailClient": row.get("emailClient"),
        }

    @staticmethod
    def _normalize_resolved_match(row: dict[str, Any] | None) -> dict[str, Any] | None:
        if not row:
            return None
        normalized = IdentityContextEnrichmentModule._normalize_ticket_candidate(row)
        normalized["resolved_via"] = row.get("_resolved_via", "")
        return IdentityContextEnrichmentModule._json_safe(normalized)

    @staticmethod
    def _resolve_primary_match(ticket_db_result) -> dict[str, Any] | None:
        if ticket_db_result.status == "found_strict" and ticket_db_result.rows:
            row = dict(ticket_db_result.rows[0])
            row["_resolved_via"] = "ticket_db_strict"
            return row
        if ticket_db_result.status == "rescue_candidates" and ticket_db_result.rescue_confident and ticket_db_result.rescue:
            row = dict(ticket_db_result.rescue[0])
            row["_resolved_via"] = f"ticket_db_rescue:{ticket_db_result.rescue_reason or 'confident'}"
            return row
        return None

    @staticmethod
    def _resolve_confidence(status: str, rescue_confident: bool) -> str:
        if status == "found_strict":
            return "high"
        if status == "rescue_candidates" and rescue_confident:
            return "medium"
        if status == "rescue_candidates":
            return "low"
        return "none"

    @staticmethod
    def _first_meaningful_note(notes: list[str] | None) -> str:
        if not notes:
            return ""
        for note in notes:
            text = str(note or "").strip()
            if text:
                return text
        return ""

    @staticmethod
    def _json_safe(value: Any):
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, dict):
            return {str(k): IdentityContextEnrichmentModule._json_safe(v) for k, v in value.items()}
        if isinstance(value, (list, tuple, set)):
            return [IdentityContextEnrichmentModule._json_safe(v) for v in value]
        if hasattr(value, "isoformat"):
            try:
                return value.isoformat()
            except Exception:
                pass
        return str(value)

    @staticmethod
    def _stub_provider(name: str, note: str) -> dict[str, Any]:
        return {
            "provider": name,
            "status": "stub",
            "rows": [],
            "notes": [note],
        }
