from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

from src.shared.common.paths import resolve_project_path


CASE_THREAD_REGISTRY_HEADERS = [
    "binding_id",
    "message_id",
    "direction",
    "sender",
    "sender_normalized",
    "subject",
    "subject_normalized",
    "sent_at",
    "in_reply_to",
    "references",
    "source_mode",
    "uid",
    "mailbox",
    "raw_path",
    "parsed_email_path",
    "case_id",
    "thread_id",
    "binding_rule",
    "matched_message_id",
    "status",
    "created_at",
]

MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
DOC_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


@dataclass
class CaseThreadRegistryStore:
    base_dir: str = "artifacts"
    relative_path: str = "state/case_thread_registry.xlsx"

    @property
    def registry_path(self) -> Path:
        return resolve_project_path(self.base_dir) / self.relative_path

    def read_all(self) -> list[dict[str, str]]:
        path = self.registry_path
        if not path.exists():
            return []
        return self._read_rows(path)

    def find_by_message_id(self, message_id: str) -> dict[str, str] | None:
        normalized = str(message_id or "").strip()
        if not normalized:
            return None
        for row in self.read_all():
            if str(row.get("message_id", "") or "").strip() == normalized:
                return row
        return None

    def append_or_get_existing(self, record: dict[str, Any]) -> tuple[dict[str, str], bool, int]:
        rows = self.read_all()
        candidate_message_id = str(record.get("message_id", "") or "").strip()
        for idx, row in enumerate(rows):
            if str(row.get("message_id", "") or "").strip() == candidate_message_id:
                return row, False, idx + 2

        normalized = {header: str(record.get(header, "") or "") for header in CASE_THREAD_REGISTRY_HEADERS}
        rows.append(normalized)
        self._write_rows(rows)
        return normalized, True, len(rows) + 1

    def next_case_id(self, rows: list[dict[str, str]] | None = None) -> str:
        return self._next_id(rows or self.read_all(), key="case_id", prefix="case")

    def next_thread_id(self, rows: list[dict[str, str]] | None = None) -> str:
        return self._next_id(rows or self.read_all(), key="thread_id", prefix="thread")

    @staticmethod
    def build_record(
        *,
        binding_id: str,
        message_id: str,
        direction: str,
        sender: str,
        sender_normalized: str,
        subject: str,
        subject_normalized: str,
        sent_at: str,
        in_reply_to: str,
        references: str,
        source_mode: str,
        uid: str,
        mailbox: str,
        raw_path: str,
        parsed_email_path: str,
        case_id: str,
        thread_id: str,
        binding_rule: str,
        matched_message_id: str,
        status: str,
    ) -> dict[str, str]:
        return {
            "binding_id": binding_id,
            "message_id": message_id,
            "direction": direction,
            "sender": sender,
            "sender_normalized": sender_normalized,
            "subject": subject,
            "subject_normalized": subject_normalized,
            "sent_at": sent_at,
            "in_reply_to": in_reply_to,
            "references": references,
            "source_mode": source_mode,
            "uid": uid,
            "mailbox": mailbox,
            "raw_path": raw_path,
            "parsed_email_path": parsed_email_path,
            "case_id": case_id,
            "thread_id": thread_id,
            "binding_rule": binding_rule,
            "matched_message_id": matched_message_id,
            "status": status,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    def _next_id(self, rows: list[dict[str, str]], key: str, prefix: str) -> str:
        max_num = 0
        pattern = re.compile(rf"^{re.escape(prefix)}-(\d+)$")
        for row in rows:
            raw_value = str(row.get(key, "") or "").strip()
            match = pattern.match(raw_value)
            if not match:
                continue
            value = int(match.group(1))
            if value > max_num:
                max_num = value
        return f"{prefix}-{max_num + 1:06d}"

    def _write_rows(self, rows: list[dict[str, str]]) -> None:
        path = self.registry_path
        path.parent.mkdir(parents=True, exist_ok=True)
        with ZipFile(path, "w", compression=ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", self._content_types_xml())
            zf.writestr("_rels/.rels", self._root_rels_xml())
            zf.writestr("xl/workbook.xml", self._workbook_xml())
            zf.writestr("xl/_rels/workbook.xml.rels", self._workbook_rels_xml())
            zf.writestr("xl/styles.xml", self._styles_xml())
            zf.writestr("xl/worksheets/sheet1.xml", self._sheet_xml(rows))

    def _read_rows(self, path: Path) -> list[dict[str, str]]:
        with ZipFile(path, "r") as zf:
            xml_data = zf.read("xl/worksheets/sheet1.xml")

        root = ET.fromstring(xml_data)
        ns = {"m": MAIN_NS}
        sheet_data = root.find("m:sheetData", ns)
        if sheet_data is None:
            return []

        raw_rows: list[list[str]] = []
        for row in sheet_data.findall("m:row", ns):
            values: list[str] = []
            for cell in row.findall("m:c", ns):
                value = ""
                inline = cell.find("m:is/m:t", ns)
                if inline is not None and inline.text is not None:
                    value = inline.text
                else:
                    v = cell.find("m:v", ns)
                    if v is not None and v.text is not None:
                        value = v.text
                values.append(value)
            raw_rows.append(values)

        if not raw_rows:
            return []

        headers = raw_rows[0]
        result: list[dict[str, str]] = []
        for row_values in raw_rows[1:]:
            padded = row_values + [""] * (len(headers) - len(row_values))
            row = {headers[i]: padded[i] for i in range(len(headers))}
            normalized = {header: str(row.get(header, "") or "") for header in CASE_THREAD_REGISTRY_HEADERS}
            result.append(normalized)
        return result

    @staticmethod
    def _content_types_xml() -> str:
        return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>
"""

    @staticmethod
    def _root_rels_xml() -> str:
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{REL_NS}">
  <Relationship Id="rId1" Type="{DOC_REL_NS}/officeDocument" Target="xl/workbook.xml"/>
</Relationships>
"""

    @staticmethod
    def _workbook_xml() -> str:
        return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="case_thread_bindings" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>
"""

    @staticmethod
    def _workbook_rels_xml() -> str:
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{REL_NS}">
  <Relationship Id="rId1" Type="{DOC_REL_NS}/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="{DOC_REL_NS}/styles" Target="styles.xml"/>
</Relationships>
"""

    @staticmethod
    def _styles_xml() -> str:
        return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>
  <fills count="1"><fill><patternFill patternType="none"/></fill></fills>
  <borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
  <cellStyleXfs count="1"><xf/></cellStyleXfs>
  <cellXfs count="1"><xf xfId="0"/></cellXfs>
</styleSheet>
"""

    def _sheet_xml(self, rows: list[dict[str, str]]) -> str:
        lines = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
            '  <sheetData>',
        ]
        headers = CASE_THREAD_REGISTRY_HEADERS
        lines.append(self._row_xml(1, headers))
        for idx, row in enumerate(rows, start=2):
            lines.append(self._row_xml(idx, [row.get(h, "") for h in headers]))
        lines.extend(['  </sheetData>', '</worksheet>'])
        return "\n".join(lines)

    @staticmethod
    def _row_xml(index: int, values: list[str]) -> str:
        cells = []
        for col_idx, value in enumerate(values, start=1):
            ref = f"{_col_name(col_idx)}{index}"
            escaped = _xml_escape(str(value))
            cells.append(f'    <c r="{ref}" t="inlineStr"><is><t>{escaped}</t></is></c>')
        return f'    <row r="{index}">\n' + "\n".join(cells) + '\n    </row>'


def _col_name(index: int) -> str:
    result = ""
    i = index
    while i > 0:
        i, rem = divmod(i - 1, 26)
        result = chr(65 + rem) + result
    return result


def _xml_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )
