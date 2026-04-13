from __future__ import annotations

import imaplib
from dataclasses import asdict
from datetime import datetime
from email import message_from_bytes
from email.header import decode_header
from email.message import Message as PyEmailMessage
from email.utils import getaddresses, parseaddr, parsedate_to_datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from src.layers.artifacts.artifact_store import ArtifactStore
from src.layers.state.import_registry_store import ImportRegistryStore
from src.shared.common.io import write_json
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
                module_ref = self.artifact_store.write_module_output(
                    run_id=context.run_id,
                    module_name=self.name,
                    payload={
                        "status": "ok",
                        "notes": notes,
                        "artifact_refs": artifact_refs,
                        "imported_count": 0,
                        "registry_path": str(self.registry_store.registry_path),
                        "imports": [],
                    },
                )
                artifact_refs.append(module_ref)
                context.artifacts.setdefault(self.name, []).extend(artifact_refs)
                return ModuleResult(
                    context=context,
                    status="ok",
                    notes=notes,
                    artifact_refs=artifact_refs,
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
            module_ref = self.artifact_store.write_module_output(
                run_id=context.run_id,
                module_name=self.name,
                payload={
                    "status": "ok",
                    "notes": notes,
                    "artifact_refs": artifact_refs,
                    "imported_count": len(imported),
                    "new_count": created_count,
                    "source_mode": source_mode,
                    "selected_message_id": context.message.message_id,
                    "registry_path": str(self.registry_store.registry_path),
                    "imports": processed_records,
                },
            )
            artifact_refs.append(module_ref)
            context.artifacts[self.name].append(module_ref)
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

        fixture_path = Path(fixture_path_raw)
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
        search_criteria = cfg.get("search_criteria", "ALL")
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

        criteria_tokens = (
            search_criteria if isinstance(search_criteria, list) else str(search_criteria).split()
        )
        if not criteria_tokens:
            criteria_tokens = ["ALL"]

        imported: list[dict[str, Any]] = []
        mail = imaplib.IMAP4_SSL(host, int(port))
        try:
            mail.login(str(username), str(password))
            status, _ = mail.select(str(mailbox), readonly=readonly)
            if status != "OK":
                raise RuntimeError(f"Failed to select mailbox '{mailbox}'")

            status, data = mail.uid("search", None, *criteria_tokens)
            if status != "OK":
                raise RuntimeError("IMAP UID SEARCH failed")

            raw_uids = data[0].decode("utf-8").strip() if data and data[0] else ""
            if not raw_uids:
                return []
            uids = raw_uids.split()[-max_messages:]

            for uid in uids:
                status, fetch_data = mail.uid("fetch", uid, "(RFC822)")
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
        body_text = self._extract_body_text(parsed)
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
        file_suffix: str,
    ) -> list[str]:
        base_dir = Path(self.artifact_store.base_dir) / "modules" / self.name / run_id
        base_dir.mkdir(parents=True, exist_ok=True)
        safe_suffix = file_suffix.replace("/", "_")

        raw_path = base_dir / f"raw_email_{safe_suffix}.eml"
        raw_path.write_bytes(raw_bytes)
        message.raw_path = str(raw_path)

        headers_path = base_dir / f"parsed_headers_{safe_suffix}.json"
        write_json(
            headers_path,
            {
                **asdict(message.headers),
                "raw_headers": raw_headers,
            },
        )

        parsed_message_path = base_dir / f"parsed_message_{safe_suffix}.json"
        write_json(
            parsed_message_path,
            {
                **asdict(message),
                "body_text_preview": body_text[:2000],
            },
        )
        return [str(raw_path), str(headers_path), str(parsed_message_path)]

    def _register_import(self, imported_item: dict[str, Any]) -> dict[str, Any]:
        message: Message = imported_item["message"]
        artifact_refs: list[str] = imported_item["artifact_refs"]
        uid = str(message.metadata.get("uid", ""))
        fixture_ref = str(message.metadata.get("fixture_ref", ""))
        mailbox = str(message.metadata.get("mailbox", ""))
        source_mode = str(message.metadata.get("source_mode", ""))
        import_id = f"imp_{uuid4().hex[:12]}"

        sent_at = message.headers.sent_at.isoformat() if message.headers.sent_at else ""
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
            parsed_headers_path=artifact_refs[1] if len(artifact_refs) > 1 else "",
            parsed_message_path=artifact_refs[2] if len(artifact_refs) > 2 else "",
            status="new",
        )
        row, created, row_number = self.registry_store.append_or_get_existing(record)

        return {
            "import_id": row["import_id"],
            "message_id": row["message_id"],
            "status": row["status"] if created else "duplicate",
            "row_number": row_number,
            "source_mode": row["source_mode"],
            "uid": row["uid"],
            "fixture_ref": row["fixture_ref"],
            "mailbox": row["mailbox"],
            "raw_path": row["raw_path"],
            "parsed_headers_path": row["parsed_headers_path"],
            "parsed_message_path": row["parsed_message_path"],
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

    @staticmethod
    def _extract_body_text(parsed: PyEmailMessage) -> str:
        if parsed.is_multipart():
            for part in parsed.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain" and part.get_content_disposition() != "attachment":
                    payload = part.get_payload(decode=True) or b""
                    charset = part.get_content_charset() or "utf-8"
                    return payload.decode(charset, errors="replace").strip()
            return ""

        payload = parsed.get_payload(decode=True)
        if isinstance(payload, bytes):
            charset = parsed.get_content_charset() or "utf-8"
            return payload.decode(charset, errors="replace").strip()
        if isinstance(payload, str):
            return payload.strip()
        return ""

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
