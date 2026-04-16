
from __future__ import annotations

import json
import os
import re
import shutil
from dataclasses import dataclass
from email import message_from_binary_file, policy
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent
LATEST_LIMIT = 10


def _try_imports():
    fitz = None
    Image = None
    pytesseract = None
    rtf_to_text = None
    try:
        import fitz as _fitz
        fitz = _fitz
    except Exception:
        pass
    try:
        from PIL import Image as _Image
        Image = _Image
    except Exception:
        pass
    try:
        import pytesseract as _pytesseract
        pytesseract = _pytesseract
    except Exception:
        pass
    try:
        from striprtf.striprtf import rtf_to_text as _rtf_to_text
        rtf_to_text = _rtf_to_text
    except Exception:
        pass
    return fitz, Image, pytesseract, rtf_to_text


FITZ, PIL_IMAGE, PYTESSERACT, RTF_TO_TEXT = _try_imports()


def detect_tesseract() -> str | None:
    candidates = [
        r"D:\soft\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    for p in candidates:
        if Path(p).exists():
            return p
    found = shutil.which("tesseract")
    return found


TESSERACT_CMD = detect_tesseract()
if PYTESSERACT and TESSERACT_CMD:
    PYTESSERACT.pytesseract.tesseract_cmd = TESSERACT_CMD


@dataclass
class ItemResult:
    filename: str
    part_index: int
    content_type: str
    inline: bool
    attachment: bool
    method: str
    text_found: bool
    preview: str
    saved_path: str
    text_path: str | None
    verdict: str


def safe_name(name: str, fallback: str) -> str:
    raw = (name or "").strip()
    if not raw:
        raw = fallback
    raw = raw.replace("/", "_").replace("\\", "_").replace(":", "_")
    raw = re.sub(r"\s+", " ", raw).strip()
    return raw[:180]


def find_latest_parsed_emails(limit: int = LATEST_LIMIT) -> list[Path]:
    patterns = ["parsed_email_*.json"]
    roots = [
        PROJECT_ROOT,
        PROJECT_ROOT / "artifacts" / "modules" / "mail_import",
    ]
    found: dict[Path, float] = {}
    for root in roots:
        if not root.exists():
            continue
        for pattern in patterns:
            for path in root.rglob(pattern):
                found[path] = path.stat().st_mtime
    ordered = sorted(found, key=lambda p: found[p], reverse=True)
    return ordered[:limit]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def get_uid(parsed_payload: dict[str, Any], parsed_path: Path) -> str:
    uid = str(parsed_payload.get("metadata", {}).get("uid", "")).strip()
    if uid:
        return uid
    m = re.search(r"parsed_email_(.+)\.json$", parsed_path.name)
    return m.group(1) if m else parsed_path.stem


def raw_email_path(parsed_payload: dict[str, Any], parsed_path: Path) -> Path | None:
    raw_path = str(parsed_payload.get("raw_path", "")).strip()
    if raw_path and Path(raw_path).exists():
        return Path(raw_path)
    uid = get_uid(parsed_payload, parsed_path)
    candidate = parsed_path.with_name(f"raw_email_{uid}.eml")
    if candidate.exists():
        return candidate
    for root in [PROJECT_ROOT, PROJECT_ROOT / "artifacts" / "modules" / "mail_import"]:
        for p in root.rglob(f"raw_email_{uid}.eml"):
            return p
    return None


def preview_text(text: str, max_len: int = 220) -> str:
    compact = re.sub(r"\s+", " ", text or "").strip()
    return compact[:max_len]


def save_text(text: str, path: Path) -> None:
    path.write_text(text, encoding="utf-8", errors="replace")


def ocr_image(image_path: Path) -> tuple[str, str]:
    if not (PYTESSERACT and PIL_IMAGE and TESSERACT_CMD):
        return "", "ocr_unavailable"
    try:
        img = PIL_IMAGE.open(image_path)
        text = PYTESSERACT.image_to_string(img, lang="rus+eng")
        return text or "", "ocr_tesseract_image"
    except Exception:
        return "", "ocr_tesseract_image_error"


def extract_pdf(pdf_path: Path) -> tuple[str, str]:
    text = ""
    used_method = "pdf_native_unavailable"
    if FITZ:
        try:
            doc = FITZ.open(pdf_path)
            text = "\n".join(page.get_text("text") for page in doc)
            used_method = "pdf_native"
        except Exception:
            text = ""
            used_method = "pdf_native_error"
    if preview_text(text):
        return text, used_method
    if not (FITZ and PYTESSERACT and PIL_IMAGE and TESSERACT_CMD):
        return "", used_method
    try:
        doc = FITZ.open(pdf_path)
        chunks = []
        for page in doc:
            pix = page.get_pixmap(matrix=FITZ.Matrix(2, 2))
            temp_png = pdf_path.with_suffix(f".page_{page.number+1}.png")
            pix.save(temp_png)
            page_text, _ = ocr_image(temp_png)
            try:
                temp_png.unlink(missing_ok=True)
            except Exception:
                pass
            if preview_text(page_text):
                chunks.append(page_text)
        text = "\n".join(chunks)
        return text, "ocr_tesseract_pdf"
    except Exception:
        return "", "ocr_tesseract_pdf_error"


def extract_rtf(rtf_path: Path) -> tuple[str, str]:
    raw = rtf_path.read_bytes()
    candidates: list[str] = []
    for enc in ("cp1251", "utf-8", "latin-1"):
        try:
            candidates.append(raw.decode(enc, errors="replace"))
        except Exception:
            pass
    for candidate in candidates:
        if RTF_TO_TEXT:
            try:
                text = RTF_TO_TEXT(candidate)
                if preview_text(text):
                    return text, "rtf_text"
            except Exception:
                pass
        if preview_text(candidate):
            return candidate, "rtf_raw_decoded"
    return "", "rtf_unavailable"


def classify_verdict(content_type: str, text: str) -> str:
    t = (text or "").lower()
    has_text = bool(preview_text(text))
    if content_type.startswith("image/"):
        if not has_text:
            return "Картинка без читаемого текста"
        document_markers = [
            "оплата", "операции", "дата", "сумма", "чек", "ticket", "order",
            "support@", "go2.by", "mooon", "билет", "карта", "qr"
        ]
        if any(m in t for m in document_markers):
            return "Картинка с полезным текстом"
        return "Картинка с текстом, но смысл надо оценивать отдельно"
    if content_type == "application/pdf":
        return "PDF с извлечённым текстом" if has_text else "PDF без текста"
    if "rtf" in content_type or "msword" in content_type or "word" in content_type:
        return "Документ с извлечённым текстом" if has_text else "Документ без текста"
    return "Текст извлечён" if has_text else "Текст не извлечён"


def process_one(parsed_path: Path) -> dict[str, Any] | None:
    payload = read_json(parsed_path)
    inventory = payload.get("attachments_inventory") or []
    if not inventory:
        return None

    raw_path = raw_email_path(payload, parsed_path)
    if not raw_path or not raw_path.exists():
        return {
            "uid": get_uid(payload, parsed_path),
            "subject": payload.get("headers", {}).get("subject", ""),
            "message_id": payload.get("message_id", ""),
            "error": "raw_email_not_found",
            "items": [],
        }

    with raw_path.open("rb") as f:
        msg = message_from_binary_file(f, policy=policy.default)

    parts = list(msg.walk())
    uid = get_uid(payload, parsed_path)
    root = raw_path.parent

    results: list[ItemResult] = []

    for item in inventory:
        part_index = int(item.get("part_index"))
        if part_index >= len(parts):
            continue
        part = parts[part_index]
        data = part.get_payload(decode=True) or b""
        content_type = str(item.get("content_type", "")).lower()
        original_name = safe_name(str(item.get("filename", "")), f"part_{part_index:02d}")
        filename = f"attachment_ocr_{uid}__{original_name}"
        saved_path = root / filename
        saved_path.write_bytes(data)

        text = ""
        method = "saved_only"

        if content_type.startswith("image/"):
            text, method = ocr_image(saved_path)
        elif content_type == "application/pdf":
            text, method = extract_pdf(saved_path)
        elif (
            saved_path.suffix.lower() == ".rtf"
            or "rtf" in content_type
            or "msword" in content_type
            or "word" in content_type
        ):
            text, method = extract_rtf(saved_path)

        text_path = None
        if preview_text(text):
            text_path = root / f"{saved_path.stem}.txt"
            save_text(text, text_path)

        verdict = classify_verdict(content_type, text)
        results.append(
            ItemResult(
                filename=filename,
                part_index=part_index,
                content_type=content_type,
                inline=bool(item.get("is_inline")),
                attachment=bool(item.get("is_attachment")),
                method=method,
                text_found=bool(preview_text(text)),
                preview=preview_text(text),
                saved_path=str(saved_path),
                text_path=str(text_path) if text_path else None,
                verdict=verdict,
            )
        )

    report = {
        "uid": uid,
        "subject": payload.get("headers", {}).get("subject", ""),
        "message_id": payload.get("message_id", ""),
        "raw_path": str(raw_path),
        "parsed_email_path": str(parsed_path),
        "items": [r.__dict__ for r in results],
    }
    report_path = root / f"attachment_ocr_report_{uid}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    report["report_path"] = str(report_path)
    return report


def print_report(report: dict[str, Any]) -> None:
    print("=" * 90)
    print(f"UID: {report.get('uid')}")
    print(f"SUBJECT: {report.get('subject') or '<empty>'}")
    print(f"MESSAGE_ID: {report.get('message_id')}")
    if report.get("error"):
        print(f"ERROR: {report['error']}")
        return
    items = report.get("items", [])
    print(f"FILES FOUND: {len(items)}")
    for idx, item in enumerate(items, start=1):
        print("-" * 90)
        print(f"[{idx}] {item['filename']}")
        print(f"TYPE: {item['content_type']}")
        print(f"ROLE: {'inline' if item['inline'] else 'attachment'}")
        print(f"OCR/TEXT: {'YES' if item['text_found'] else 'NO'}")
        print(f"METHOD: {item['method']}")
        print(f"VERDICT: {item['verdict']}")
        print(f"PREVIEW: {item['preview'] if item['preview'] else '<empty>'}")
        print(f"FILE: {item['saved_path']}")
        if item.get("text_path"):
            print(f"TEXT FILE: {item['text_path']}")
    print("-" * 90)
    print(f"REPORT JSON: {report.get('report_path')}")


def main() -> None:
    parsed_files = find_latest_parsed_emails(LATEST_LIMIT)

    print("=" * 90)
    print("ATTACHMENT OCR CHECK - READABLE")
    print("=" * 90)
    print(f"project_root: {PROJECT_ROOT}")
    print(f"selected_latest_parsed_email_files: {len(parsed_files)}")
    print("write_mode: in_place_next_to_source_email")
    print(f"tesseract: {TESSERACT_CMD or 'NOT FOUND'}")

    shown = 0
    for parsed_path in parsed_files:
        report = process_one(parsed_path)
        if not report:
            continue
        if not report.get("items") and not report.get("error"):
            continue
        print_report(report)
        shown += 1

    print("=" * 90)
    print(f"DONE. SHOWN REPORTS: {shown}")
    print("=" * 90)


if __name__ == "__main__":
    main()
