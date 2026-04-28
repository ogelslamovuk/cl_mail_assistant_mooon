from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from email import message_from_binary_file, policy
from pathlib import Path
from typing import Any

from src.shared.common.message_dossier import load_message_record, resolve_dossier_path, write_message_dossier
from src.shared.contracts.module_contract import ModuleResult
from src.shared.models.pipeline_context import PipelineContext


try:
    import fitz as _fitz  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    _fitz = None

try:
    from PIL import Image as _pil_image  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    _pil_image = None

try:
    import pytesseract as _pytesseract  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    _pytesseract = None

try:
    from striprtf.striprtf import rtf_to_text as _rtf_to_text  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    _rtf_to_text = None


FITZ = _fitz
PIL_IMAGE = _pil_image
PYTESSERACT = _pytesseract
RTF_TO_TEXT = _rtf_to_text


ALLOWED_METHODS = {
    "ocr_tesseract_image",
    "ocr_tesseract_image_error",
    "ocr_unavailable",
    "pdf_native",
    "pdf_native_error",
    "pdf_native_unavailable",
    "ocr_tesseract_pdf",
    "ocr_tesseract_pdf_error",
    "rtf_text",
    "rtf_raw_decoded",
    "rtf_unavailable",
    "saved_only",
    "unsupported_type",
}


@dataclass
class ItemExtractionResult:
    part_index: int
    filename_original: str
    filename_saved: str
    content_type: str
    content_disposition: str
    is_inline: bool
    is_attachment: bool
    saved_path: str
    text_found: bool
    text_path: str
    text_preview: str
    extraction_method: str
    error: str
    skip_reason: str


class AttachmentExtractionModule:
    name = "attachment_extraction"

    def __init__(self, parsed_email_path: str, raw_email_path: str | None = None) -> None:
        self.parsed_email_path = parsed_email_path
        self.raw_email_path = raw_email_path
        self._configure_tesseract()

    def run(self, context: PipelineContext) -> ModuleResult:
        parsed_path = Path(self.parsed_email_path)
        if not parsed_path.exists():
            return ModuleResult(context=context, status="error", notes=[f"parsed_email missing: {parsed_path}"])

        try:
            payload = load_message_record(parsed_path)
        except Exception as exc:
            return ModuleResult(context=context, status="error", notes=[f"message record unreadable: {exc}"])

        raw_path = self._resolve_raw_path(payload, parsed_path)
        if not raw_path:
            return ModuleResult(context=context, status="error", notes=["raw_email missing"])

        try:
            with raw_path.open("rb") as handle:
                msg = message_from_binary_file(handle, policy=policy.default)
        except Exception as exc:
            return ModuleResult(context=context, status="error", notes=[f"raw_email open/parse failed: {exc}"])

        parts = list(msg.walk())
        uid = self._resolve_uid(payload, parsed_path)
        dossier_path = resolve_dossier_path(parsed_path, uid)
        subject = str((payload.get("headers") or {}).get("subject", "") or "")
        message_id = str(payload.get("message_id", "") or "")
        attachments_inventory = payload.get("attachments_inventory") or []
        output_root = raw_path.parent

        item_results: list[dict[str, Any]] = []
        artifact_refs: list[str] = []

        for raw_item in attachments_inventory:
            result = self._process_one_item(item=raw_item, parts=parts, output_root=output_root, uid=uid)
            item_results.append(result.__dict__)
            if result.saved_path:
                artifact_refs.append(result.saved_path)
            if result.text_path:
                artifact_refs.append(result.text_path)

        report = {
            "uid": uid,
            "message_id": message_id,
            "subject": subject,
            "raw_path": str(raw_path),
            "message_file_path": str(dossier_path),
            "items": item_results,
        }

        payload.setdefault("modules", {})[self.name] = report
        write_message_dossier(dossier_path, payload)
        artifact_refs.append(str(dossier_path))

        context.artifacts.setdefault(self.name, []).append(str(dossier_path))
        context.enrichment.setdefault("attachment_extraction", report)

        metrics = {
            "uid": uid,
            "message_id": message_id,
            "subject": subject,
            "raw_path": str(raw_path),
            "parsed_email_path": str(dossier_path),
            "report_path": str(dossier_path),
            "dossier_path": str(dossier_path),
            "items_count": len(item_results),
            "items": item_results,
        }
        return ModuleResult(
            context=context,
            status="ok",
            notes=[f"attachment_extraction processed items={len(item_results)} uid={uid}"],
            artifact_refs=artifact_refs,
            metrics=metrics,
        )

    def _process_one_item(self, item: dict[str, Any], parts: list[Any], output_root: Path, uid: str) -> ItemExtractionResult:
        part_index_raw = item.get("part_index")
        filename_original = str(item.get("filename", "") or "")
        content_type = str(item.get("content_type", "") or "").lower()
        content_disposition = str(item.get("content_disposition", "") or "").lower()
        is_inline = bool(item.get("is_inline"))
        is_attachment = bool(item.get("is_attachment"))

        if part_index_raw is None:
            return self._item_error(-1, filename_original, content_type, content_disposition, is_inline, is_attachment, "missing_part_index")

        try:
            part_index = int(part_index_raw)
        except Exception:
            return self._item_error(-1, filename_original, content_type, content_disposition, is_inline, is_attachment, "invalid_part_index")

        if part_index < 0 or part_index >= len(parts):
            return self._item_error(part_index, filename_original, content_type, content_disposition, is_inline, is_attachment, "part_index_not_found")

        part = parts[part_index]
        data = part.get_payload(decode=True)
        if not isinstance(data, bytes) or not data:
            return self._item_error(part_index, filename_original, content_type, content_disposition, is_inline, is_attachment, "missing_payload")

        safe_original = self._sanitize_filename(filename_original, fallback=f"part_{part_index}")
        saved_name = f"attachment_extraction_{uid}__{safe_original}"
        saved_path = output_root / saved_name
        saved_path.write_bytes(data)

        text = ""
        method = "saved_only"
        skip_reason = ""

        if content_type in {"image/png", "image/jpeg"}:
            text, method = self._ocr_image(saved_path)
        elif content_type == "application/pdf":
            text, method = self._extract_pdf(saved_path)
        elif self._is_rtf_document_like(saved_path=saved_path, content_type=content_type):
            text, method = self._extract_rtf(saved_path)
        elif content_type.startswith("image/"):
            text, method = self._ocr_image(saved_path)
        else:
            method = "unsupported_type"
            skip_reason = "unsupported_content_type"

        if method not in ALLOWED_METHODS:
            method = "saved_only"

        normalized_text = self._normalize_text(text)
        text_found = bool(normalized_text)
        text_path = ""
        if text_found:
            text_file_name = f"attachment_extraction_{uid}__{Path(safe_original).stem}.txt"
            text_file_path = output_root / text_file_name
            text_file_path.write_text(text, encoding="utf-8", errors="replace")
            text_path = str(text_file_path)

        return ItemExtractionResult(
            part_index=part_index,
            filename_original=filename_original,
            filename_saved=saved_name,
            content_type=content_type,
            content_disposition=content_disposition,
            is_inline=is_inline,
            is_attachment=is_attachment,
            saved_path=str(saved_path),
            text_found=text_found,
            text_path=text_path,
            text_preview=normalized_text[:220],
            extraction_method=method,
            error="",
            skip_reason=skip_reason,
        )

    @staticmethod
    def _item_error(
        part_index: int,
        filename_original: str,
        content_type: str,
        content_disposition: str,
        is_inline: bool,
        is_attachment: bool,
        error: str,
    ) -> ItemExtractionResult:
        return ItemExtractionResult(
            part_index=part_index,
            filename_original=filename_original,
            filename_saved="",
            content_type=content_type,
            content_disposition=content_disposition,
            is_inline=is_inline,
            is_attachment=is_attachment,
            saved_path="",
            text_found=False,
            text_path="",
            text_preview="",
            extraction_method="saved_only",
            error=error,
            skip_reason="",
        )

    def _extract_pdf(self, pdf_path: Path) -> tuple[str, str]:
        extracted = ""
        method = "pdf_native_unavailable"

        if FITZ is not None:
            try:
                with FITZ.open(pdf_path) as doc:
                    extracted = "\n".join(page.get_text("text") for page in doc)
                method = "pdf_native"
            except Exception:
                extracted = ""
                method = "pdf_native_error"

        if len(self._normalize_text(extracted)) >= 80:
            return extracted, method

        if not self._ocr_available() or FITZ is None:
            return extracted, method

        try:
            with FITZ.open(pdf_path) as doc:
                chunks: list[str] = []
                for page in doc:
                    pix = page.get_pixmap(matrix=FITZ.Matrix(2, 2))
                    temp_path = pdf_path.with_suffix(f".page_{page.number + 1}.png")
                    pix.save(temp_path)
                    page_text, _ = self._ocr_image(temp_path)
                    try:
                        temp_path.unlink(missing_ok=True)
                    except Exception:
                        pass
                    if self._normalize_text(page_text):
                        chunks.append(page_text)
            return "\n".join(chunks), "ocr_tesseract_pdf"
        except Exception:
            return "", "ocr_tesseract_pdf_error"

    def _ocr_image(self, image_path: Path) -> tuple[str, str]:
        if not self._ocr_available():
            return "", "ocr_unavailable"
        try:
            img = PIL_IMAGE.open(image_path)
            text = PYTESSERACT.image_to_string(img, lang="rus+eng")
            return text or "", "ocr_tesseract_image"
        except Exception:
            return "", "ocr_tesseract_image_error"

    def _extract_rtf(self, file_path: Path) -> tuple[str, str]:
        raw = file_path.read_bytes()
        for enc in ("cp1251", "utf-8", "latin-1"):
            try:
                candidate = raw.decode(enc, errors="replace")
            except Exception:
                continue
            if RTF_TO_TEXT is not None:
                try:
                    parsed = RTF_TO_TEXT(candidate)
                    if self._normalize_text(parsed):
                        return parsed, "rtf_text"
                except Exception:
                    pass
            if self._normalize_text(candidate):
                return candidate, "rtf_raw_decoded"
        return "", "rtf_unavailable"

    @staticmethod
    def _is_rtf_document_like(saved_path: Path, content_type: str) -> bool:
        suffix = saved_path.suffix.lower()
        return suffix == ".rtf" or "rtf" in content_type or "msword" in content_type or "word" in content_type

    @staticmethod
    def _normalize_text(text: str) -> str:
        return re.sub(r"\s+", " ", text or "").strip()

    @staticmethod
    def _resolve_uid(payload: dict[str, Any], parsed_path: Path) -> str:
        metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
        uid = str(metadata.get("uid", "") or "").strip()
        if uid:
            return uid
        match = re.search(r"(?:parsed_email|message)_(.+)\.(?:json|md)$", parsed_path.name)
        return match.group(1) if match else parsed_path.stem

    def _resolve_raw_path(self, payload: dict[str, Any], parsed_path: Path) -> Path | None:
        explicit_raw = str(self.raw_email_path or "").strip()
        if explicit_raw:
            path = Path(explicit_raw)
            if path.exists():
                return path

        raw_from_json = str(payload.get("raw_path", "") or "").strip()
        if raw_from_json:
            path = Path(raw_from_json)
            if path.exists():
                return path

        uid = self._resolve_uid(payload, parsed_path)
        candidate = parsed_path.with_name(f"raw_email_{uid}.eml")
        if candidate.exists():
            return candidate
        return None

    @staticmethod
    def _sanitize_filename(name: str, fallback: str, max_len: int = 180) -> str:
        raw = (name or "").strip() or fallback
        raw = raw.replace("/", "_").replace("\\", "_").replace(":", "_")
        raw = re.sub(r"\s+", " ", raw).strip()

        p = Path(raw)
        stem = p.stem or fallback
        suffix = p.suffix
        limit_for_stem = max(1, max_len - len(suffix))
        return f"{stem[:limit_for_stem]}{suffix}" if suffix else stem[:max_len]

    def _configure_tesseract(self) -> None:
        if PYTESSERACT is None:
            return
        cmd = self._detect_tesseract()
        if cmd:
            PYTESSERACT.pytesseract.tesseract_cmd = cmd

    @staticmethod
    def _detect_tesseract() -> str | None:
        candidates = [
            r"D:\soft\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        for candidate in candidates:
            if Path(candidate).exists():
                return candidate
        return shutil.which("tesseract")

    @staticmethod
    def _ocr_available() -> bool:
        return bool(PYTESSERACT and PIL_IMAGE and AttachmentExtractionModule._detect_tesseract())
