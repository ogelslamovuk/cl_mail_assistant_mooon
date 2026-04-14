from __future__ import annotations

import imaplib
import re
from dataclasses import asdict
from datetime import datetime
from email import message_from_bytes
from email.header import decode_header
from email.message import Message as PyEmailMessage
from email.utils import getaddresses, parseaddr, parsedate_to_datetime
from html import unescape
from pathlib import Path
from typing import Any
from uuid import uuid4

from src.layers.artifacts.artifact_store import ArtifactStore
from src.layers.state.import_registry_store import ImportRegistryStore
from src.shared.common.io import write_json
from src.shared.common.paths import resolve_project_path
from src.shared.contracts.module_contract import ModuleResult
from src.shared.models.entities import EmailHeaders, Message
from src.shared.models.pipeline_context import PipelineContext


class MailImportModule:
    name = "mail_import"

    def __init__(
        self,
        config: dict[str, Any] | None = None,
        artifacts_dir: str = "artifacts",
        run_options: dict[str, Any] | None = None,
    ) -> None:
        self.config = config or {}
        self.artifact_store = ArtifactStore(base_dir=artifacts_dir)
        self.registry_store = ImportRegistryStore(base_dir=artifacts_dir)
        self.run_options = run_options or {}

    def run(self, context: PipelineContext) -> ModuleResult:
        try:
            cfg = self._resolved_config()

            if not cfg.get("enabled", True):
                notes = ["mail_import disabled by config."]
                return ModuleResult(
                    context=context,
                    status="skipped",
                    notes=notes,
                    artifact_refs=[],
                    metrics={
                        "processed_count": 0,
                        "new_count": 0,
                        "imports": [],
                        "registry_path": str(self.registry_store.registry_path),
                        "source_mode": str(cfg.get("mode", "fixture")).lower(),
                    },
                )

            source_mode = str(cfg.get("mode", "fixture")).lower()
            if source_mode not in {"fixture", "imap"}:
                raise ValueError(f"Unsupported mail_import.mode: {source_mode}")

            artifact_refs: list[str] = []
            if source_mode == "fixture":
                imported = self._import_from_fixture(cfg, run_id=context.run_id)
            else:
                imported = self._import_from_imap(cfg, run_id=context.run_id)

            processed_records: list[dict[str, Any]] = []
            if not imported:
                notes = ["No messages imported."]
                context.artifacts.setdefault(self.name, [])
                return ModuleResult(
                    context=context,
                    status="ok",
                    notes=notes,
                    artifact_refs=[],
                    metrics={
                        "processed_count": 0,
                        "new_count": 0,
                        "imports": [],
                        "registry_path": str(self.registry_store.registry_path),
                        "source_mode": source_mode,
                    },
                )

            created_count = 0
            for item in imported:
                registry_payload = self._register_import(item)
                processed_records.append(registry_payload)
                if registry_payload["status"] == "new":
                    created_count += 1

            first = imported[0]
            context.message = first["message"]
            for item in imported:
                artifact_refs.extend(item["artifact_refs"])
            context.artifacts.setdefault(self.name, []).extend(artifact_refs)

            notes = [
                f"Processed {len(imported)} message(s) via {source_mode}.",
                f"New registry rows: {created_count}.",
                f"Context.message set to Message-ID={context.message.message_id}.",
            ]
            return ModuleResult(
                context=context,
                status="ok",
                notes=notes,
                artifact_refs=artifact_refs,
                metrics={
                    "processed_count": len(imported),
                    "new_count": created_count,
                    "imports": processed_records,
                    "registry_path": str(self.registry_store.registry_path),
                    "source_mode": source_mode,
                },
            )
        except Exception as exc:
            notes = [f"mail_import failed: {exc}"]
            return ModuleResult(
                context=context,
                status="error",
                notes=notes,
                artifact_refs=[],
                metrics={
                    "processed_count": 0,
                    "new_count": 0,
                    "imports": [],
                    "registry_path": str(self.registry_store.registry_path),
                },
            )

    def _resolved_config(self) -> dict[str, Any]:
        cfg = dict(self.config)
        for key, value in self.run_options.items():
            if value is not None:
                cfg[key] = value
        return cfg

    def _import_from_fixture(self, cfg: dict[str, Any], run_id: str) -> list[dict[str, Any]]:
        fixture_path_raw = cfg.get("fixture_path")
        if not fixture_path_raw:
            raise ValueError("fixture mode requires 'fixture_path'")

        fixture_path = resolve_project_path(fixture_path_raw)
        if not fixture_path.exists():
            raise FileNotFoundError(f"Fixture file not found: {fixture_path}")

        raw_bytes = fixture_path.read_bytes()
        fixture_ref = str(cfg.get("fixture_ref", fixture_path.stem))
        message, refs = self._build_message_with_artifacts(
            raw_bytes=raw_bytes,
            uid="",
            fixture_ref=fixture_ref,
            mailbox=str(cfg.get("mailbox", "fixture")),
            run_id=run_id,
            source_mode="fixture",
            email_address=str(cfg.get("email_address", "")),
            file_suffix=fixture_path.stem,
        )
        return [{"message": message, "artifact_refs": refs}]

    def _import_from_imap(self, cfg: dict[str, Any], run_id: str) -> list[dict[str, Any]]:
        host = cfg.get("imap_host")
        port = cfg.get("imap_port", 993)
        username = cfg.get("imap_username")
        password = cfg.get("app_password")
        mailbox = cfg.get("mailbox", "INBOX")
        readonly = bool(cfg.get("readonly", True))
        max_messages = int(cfg.get("max_messages_per_run", 1))

        missing = [
            field
            for field, value in {
                "imap_host": host,
                "imap_username": username,
                "app_password": password,
            }.items()
            if not value
        ]
        if missing:
            raise ValueError(f"imap mode missing required config fields: {', '.join(missing)}")

        if max_messages <= 0:
            return []

        imported: list[dict[str, Any]] = []
        mail = imaplib.IMAP4_SSL(host, int(port))
        try:
            mail.login(str(username), str(password))
            status, _ = mail.select(str(mailbox), readonly=readonly)
            if status != "OK":
                raise RuntimeError(f"Failed to select mailbox '{mailbox}'")

            last_processed_uid = self.registry_store.get_max_imap_uid_for_mailbox(str(mailbox))
            if last_processed_uid is None:
                all_uids = self._imap_search_all_uids(mail)
                bootstrap_uid = all_uids[-1] if all_uids else 0
                self._bootstrap_imap_cursor(mailbox=str(mailbox), cursor_uid=bootstrap_uid)
                return []

            all_uids = self._imap_search_all_uids(mail)
            if not all_uids:
                return []

            uids = [uid for uid in all_uids if uid > last_processed_uid]
            if not uids:
                return []
            uids = uids[:max_messages]

            for uid in uids:
                status, fetch_data = mail.uid("fetch", str(uid), "(RFC822)")
                if status != "OK":
                    continue
                raw_bytes = self._extract_rfc822_bytes(fetch_data)
                if not raw_bytes:
                    continue

                message, refs = self._build_message_with_artifacts(
                    raw_bytes=raw_bytes,
                    uid=str(uid),
                    fixture_ref="",
                    mailbox=str(mailbox),
                    run_id=run_id,
                    source_mode="imap",
                    email_address=str(cfg.get("email_address", "")),
                    file_suffix=str(uid),
                )
                imported.append({"message": message, "artifact_refs": refs})
        finally:
            try:
                mail.logout()
            except Exception:
                pass

        return imported

    @staticmethod
    def _imap_search_all_uids(mail: imaplib.IMAP4_SSL) -> list[int]:
        status, data = mail.uid("search", None, "ALL")
        if status != "OK":
            raise RuntimeError("IMAP UID SEARCH failed")
        raw_uids = data[0].decode("utf-8").strip() if data and data[0] else ""
        if not raw_uids:
            return []
        uids = [int(uid) for uid in raw_uids.split() if uid.isdigit()]
        uids.sort()
        return uids

    def _bootstrap_imap_cursor(self, mailbox: str, cursor_uid: int) -> None:
        record = self.registry_store.build_record(
            import_id=f"bootstrap_{uuid4().hex[:12]}",
            source_mode="imap",
            uid=str(cursor_uid),
            fixture_ref="",
            message_id=f"__bootstrap_cursor__:{mailbox}",
            sender="",
            subject="",
            sent_at="",
            mailbox=mailbox,
            raw_path="",
            parsed_email_path="",
            status="bootstrap_cursor",
        )
        self.registry_store.append_or_get_existing(record)

    @staticmethod
    def _extract_rfc822_bytes(fetch_data: list[Any]) -> bytes | None:
        for item in fetch_data:
            if isinstance(item, tuple) and len(item) >= 2 and isinstance(item[1], bytes):
                return item[1]
        return None

    def _build_message_with_artifacts(
        self,
        raw_bytes: bytes,
        uid: str,
        fixture_ref: str,
        mailbox: str,
        run_id: str,
        source_mode: str,
        email_address: str,
        file_suffix: str,
    ) -> tuple[Message, list[str]]:
        parsed = message_from_bytes(raw_bytes)
        raw_headers = self._serialize_raw_headers(parsed)
        analysis = self._analyze_mime(parsed)
        body_text = str(analysis["body_text"])
        headers = self._build_headers(parsed)
        direction = self._detect_direction(headers.sender, email_address)

        message = Message(
            message_id=headers.message_id,
            direction=direction,
            headers=headers,
            body_text=body_text,
            metadata={
                "uid": uid,
                "fixture_ref": fixture_ref,
                "mailbox": mailbox,
                "source_mode": source_mode,
            },
        )

        refs = self._write_message_artifacts(
            run_id=run_id,
            message=message,
            raw_bytes=raw_bytes,
            raw_headers=raw_headers,
            body_text=body_text,
            mime_analysis=analysis,
            file_suffix=file_suffix,
        )
        if refs:
            message.raw_path = refs[0]
            message.metadata["artifact_refs"] = refs
        return message, refs

    def _write_message_artifacts(
        self,
        run_id: str,
        message: Message,
        raw_bytes: bytes,
        raw_headers: str,
        body_text: str,
        mime_analysis: dict[str, Any],
        file_suffix: str,
    ) -> list[str]:
        base_dir = Path(self.artifact_store.base_dir) / "modules" / self.name / run_id
        base_dir.mkdir(parents=True, exist_ok=True)
        safe_suffix = file_suffix.replace("/", "_")

        raw_path = base_dir / f"raw_email_{safe_suffix}.eml"
        raw_path.write_bytes(raw_bytes)
        message.raw_path = str(raw_path)

        parsed_email_path = base_dir / f"parsed_email_{safe_suffix}.json"
        write_json(
            parsed_email_path,
            {
                "message_id": message.message_id,
                "direction": message.direction,
                "headers": asdict(message.headers),
                "body_text": body_text,
                "raw_path": str(raw_path),
                "raw_headers": raw_headers,
                "metadata": dict(message.metadata),
                "body_text_preview": body_text[:2000],
                "has_text_plain": bool(mime_analysis["has_text_plain"]),
                "has_text_html": bool(mime_analysis["has_text_html"]),
                "preferred_body_source": str(mime_analysis["preferred_body_source"]),
                "body_sources": list(mime_analysis["body_sources"]),
                "mime_parts": list(mime_analysis["mime_parts"]),
                "has_attachments": bool(mime_analysis["has_attachments"]),
                "has_inline_parts": bool(mime_analysis["has_inline_parts"]),
                "attachments_inventory": list(mime_analysis["attachments_inventory"]),
                "is_bounce": bool(mime_analysis["is_bounce"]),
                "is_auto_reply": bool(mime_analysis["is_auto_reply"]),
                "is_mailing_like": bool(mime_analysis["is_mailing_like"]),
                "is_system_generated_likely": bool(mime_analysis["is_system_generated_likely"]),
                "bounce_reasons": list(mime_analysis["bounce_reasons"]),
                "auto_reply_reasons": list(mime_analysis["auto_reply_reasons"]),
                "mailing_like_reasons": list(mime_analysis["mailing_like_reasons"]),
                "system_generated_reasons": list(mime_analysis["system_generated_reasons"]),
            },
        )
        return [str(raw_path), str(parsed_email_path)]

    def _register_import(self, imported_item: dict[str, Any]) -> dict[str, Any]:
        message: Message = imported_item["message"]
        artifact_refs: list[str] = imported_item["artifact_refs"]
        uid = str(message.metadata.get("uid", ""))
        fixture_ref = str(message.metadata.get("fixture_ref", ""))
        mailbox = str(message.metadata.get("mailbox", ""))
        source_mode = str(message.metadata.get("source_mode", ""))
        import_id = f"imp_{uuid4().hex[:12]}"

        sent_at = message.headers.sent_at.isoformat() if message.headers.sent_at else ""
        parsed_email_path = artifact_refs[1] if len(artifact_refs) > 1 else ""
        record = self.registry_store.build_record(
            import_id=import_id,
            source_mode=source_mode,
            uid=uid,
            fixture_ref=fixture_ref,
            message_id=message.message_id,
            sender=message.headers.sender,
            subject=message.headers.subject,
            sent_at=sent_at,
            mailbox=mailbox,
            raw_path=artifact_refs[0] if len(artifact_refs) > 0 else "",
            parsed_email_path=parsed_email_path,
            status="new",
        )
        row, created, row_number = self.registry_store.append_or_get_existing(record)

        return {
            "import_id": row["import_id"],
            "message_id": row["message_id"],
            "sender": row["sender"],
            "subject": row["subject"],
            "sent_at": row["sent_at"],
            "status": row["status"] if created else "duplicate",
            "row_number": row_number,
            "source_mode": row["source_mode"],
            "uid": row["uid"],
            "fixture_ref": row["fixture_ref"],
            "mailbox": row["mailbox"],
            "raw_path": row["raw_path"],
            "parsed_email_path": row["parsed_email_path"],
            "registry_path": str(self.registry_store.registry_path),
        }

    @staticmethod
    def _build_headers(parsed: PyEmailMessage) -> EmailHeaders:
        sender = parseaddr(parsed.get("From", ""))[1] or MailImportModule._decode_mime(parsed.get("From", ""))
        to_list = [addr for _, addr in getaddresses(parsed.get_all("To", [])) if addr]
        cc_list = [addr for _, addr in getaddresses(parsed.get_all("Cc", [])) if addr]
        references = [x.strip() for x in parsed.get("References", "").split() if x.strip()]
        message_id = MailImportModule._decode_mime(parsed.get("Message-ID", "")).strip() or "missing-message-id"

        sent_at: datetime | None = None
        raw_date = parsed.get("Date")
        if raw_date:
            try:
                sent_at = parsedate_to_datetime(raw_date)
            except Exception:
                sent_at = None

        return EmailHeaders(
            message_id=message_id,
            in_reply_to=MailImportModule._decode_mime(parsed.get("In-Reply-To")),
            references=references,
            subject=MailImportModule._decode_mime(parsed.get("Subject")),
            sender=sender,
            sent_at=sent_at,
            to=to_list,
            cc=cc_list,
        )

    def _analyze_mime(self, parsed: PyEmailMessage) -> dict[str, Any]:
        mime_parts: list[dict[str, Any]] = []
        attachments_inventory: list[dict[str, Any]] = []
        plain_candidates: list[str] = []
        html_candidates: list[str] = []
        body_sources: list[str] = []

        for part_index, part in enumerate(parsed.walk()):
            content_type = part.get_content_type().lower()
            disposition_raw = part.get_content_disposition() or ""
            content_disposition = disposition_raw.lower()
            raw_filename = part.get_filename()
            decoded_filename = self._decode_mime(raw_filename) if raw_filename else ""
            filename = decoded_filename or (raw_filename or "")
            content_id = (part.get("Content-ID") or "").strip().strip("<>")
            charset = part.get_content_charset() or ""
            is_multipart = part.is_multipart()
            payload = part.get_payload(decode=True)
            payload_bytes = payload if isinstance(payload, bytes) else b""
            size_bytes = len(payload_bytes)

            is_attachment = content_disposition == "attachment" or (
                bool(filename) and content_disposition != "inline" and not content_type.startswith("text/")
            )
            is_inline = content_disposition == "inline" or (
                bool(content_id) and content_disposition != "attachment" and not is_attachment
            )

            mime_parts.append(
                {
                    "part_index": part_index,
                    "content_type": content_type,
                    "content_disposition": content_disposition,
                    "filename": filename or "",
                    "content_id": content_id,
                    "charset": charset,
                    "is_multipart": is_multipart,
                    "size_bytes": size_bytes,
                    "is_inline": is_inline,
                    "is_attachment": is_attachment,
                }
            )

            if is_attachment or is_inline:
                attachments_inventory.append(
                    {
                        "part_index": part_index,
                        "filename": filename or "",
                        "content_type": content_type,
                        "content_disposition": content_disposition,
                        "content_id": content_id,
                        "is_inline": is_inline,
                        "is_attachment": is_attachment,
                        "size_bytes": size_bytes,
                    }
                )

            if is_multipart:
                continue

            if content_type == "text/plain" and not is_attachment:
                text = self._decode_text_part(part, payload_bytes)
                if text:
                    plain_candidates.append(text)
            elif content_type == "text/html" and not is_attachment:
                html_text = self._html_to_text(self._decode_text_part(part, payload_bytes))
                if html_text:
                    html_candidates.append(html_text)

        has_text_plain = bool(plain_candidates)
        has_text_html = bool(html_candidates)
        preferred_body_source = "none"
        body_text = ""
        if has_text_plain:
            preferred_body_source = "text/plain"
            body_sources.append("text/plain")
            body_text = plain_candidates[0]
            if has_text_html:
                body_sources.append("text/html")
        elif has_text_html:
            preferred_body_source = "text/html"
            body_sources.append("text/html")
            body_text = html_candidates[0]

        flags = self._build_technical_flags(parsed, mime_parts)

        return {
            "body_text": body_text.strip(),
            "has_text_plain": has_text_plain,
            "has_text_html": has_text_html,
            "preferred_body_source": preferred_body_source,
            "body_sources": body_sources,
            "mime_parts": mime_parts,
            "has_attachments": any(item["is_attachment"] for item in attachments_inventory),
            "has_inline_parts": any(item["is_inline"] for item in attachments_inventory),
            "attachments_inventory": attachments_inventory,
            **flags,
        }

    @staticmethod
    def _decode_text_part(part: PyEmailMessage, payload_bytes: bytes) -> str:
        if payload_bytes:
            charset = part.get_content_charset() or "utf-8"
            return payload_bytes.decode(charset, errors="replace").strip()
        payload = part.get_payload()
        if isinstance(payload, str):
            return payload.strip()
        return ""

    @staticmethod
    def _html_to_text(html: str) -> str:
        if not html:
            return ""
        text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", html)
        text = re.sub(r"(?i)<br\s*/?>", "\n", text)
        text = re.sub(r"(?i)</p\s*>", "\n", text)
        text = re.sub(r"(?s)<[^>]+>", " ", text)
        text = unescape(text)
        text = re.sub(r"[ \\t\\r\\f\\v]+", " ", text)
        text = re.sub(r"\n\s*\n+", "\n\n", text)
        return text.strip()

    def _build_technical_flags(self, parsed: PyEmailMessage, mime_parts: list[dict[str, Any]]) -> dict[str, Any]:
        subject = self._decode_mime(parsed.get("Subject", "")).lower()
        from_raw = self._decode_mime(parsed.get("From", "")).lower()
        sender_addr = parseaddr(parsed.get("From", ""))[1].lower()
        auto_submitted = str(parsed.get("Auto-Submitted", "")).lower()
        precedence = str(parsed.get("Precedence", "")).lower()

        bounce_reasons: list[str] = []
        auto_reply_reasons: list[str] = []
        mailing_like_reasons: list[str] = []
        system_generated_reasons: list[str] = []

        if any(part["content_type"] == "multipart/report" for part in mime_parts):
            bounce_reasons.append("mime contains multipart/report")
        if "report-type=delivery-status" in str(parsed.get("Content-Type", "")).lower():
            bounce_reasons.append("content-type report-type=delivery-status")
        if any(part["content_type"] == "message/delivery-status" for part in mime_parts):
            bounce_reasons.append("mime contains message/delivery-status")
        if "mailer-daemon" in from_raw:
            bounce_reasons.append("from contains mailer-daemon")
        if "undelivered mail returned to sender" in subject:
            bounce_reasons.append("subject indicates undelivered mail")

        if "auto-replied" in auto_submitted:
            auto_reply_reasons.append("Auto-Submitted=auto-replied")
        if parsed.get("X-Auto-Response-Suppress"):
            auto_reply_reasons.append("X-Auto-Response-Suppress header is present")
        if any(token in subject for token in ["auto-reply", "out of office", "vacation reply", "autoreply"]):
            auto_reply_reasons.append("subject matches autoresponder pattern")
        if parsed.get("X-Autoreply") or parsed.get("X-Autorespond"):
            auto_reply_reasons.append("autoresponder header is present")

        if parsed.get("List-Unsubscribe"):
            mailing_like_reasons.append("List-Unsubscribe header is present")
        if parsed.get("List-Id"):
            mailing_like_reasons.append("List-Id header is present")
        if precedence in {"bulk", "list", "junk"}:
            mailing_like_reasons.append(f"Precedence={precedence}")
        if parsed.get("List-Post") or parsed.get("List-Help"):
            mailing_like_reasons.append("list management header is present")

        if any(token in sender_addr for token in ["no-reply", "noreply", "do-not-reply"]):
            system_generated_reasons.append("sender address looks like no-reply")
        if auto_submitted:
            system_generated_reasons.append("Auto-Submitted header is present")
        if bounce_reasons:
            system_generated_reasons.append("bounce-like signals detected")
        if "daemon" in from_raw:
            system_generated_reasons.append("from contains daemon marker")

        return {
            "is_bounce": bool(bounce_reasons),
            "is_auto_reply": bool(auto_reply_reasons),
            "is_mailing_like": bool(mailing_like_reasons),
            "is_system_generated_likely": bool(system_generated_reasons),
            "bounce_reasons": bounce_reasons,
            "auto_reply_reasons": auto_reply_reasons,
            "mailing_like_reasons": mailing_like_reasons,
            "system_generated_reasons": system_generated_reasons,
        }

    @staticmethod
    def _serialize_raw_headers(parsed: PyEmailMessage) -> str:
        return "".join(f"{k}: {v}\n" for k, v in parsed.items())

    @staticmethod
    def _decode_mime(value: str | None) -> str:
        if not value:
            return ""
        decoded_parts: list[str] = []
        for part, encoding in decode_header(value):
            if isinstance(part, bytes):
                decoded_parts.append(part.decode(encoding or "utf-8", errors="replace"))
            else:
                decoded_parts.append(part)
        return "".join(decoded_parts).strip()

    @staticmethod
    def _detect_direction(sender: str, email_address: str) -> str:
        if not sender or not email_address:
            return "inbound"
        return "outbound" if sender.lower() == email_address.lower() else "inbound"
