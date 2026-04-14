from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

from src.shared.common.paths import import_registry_path, resolve_project_path


REGISTRY_HEADERS = [
    "import_id",
    "source_mode",
    "uid",
    "fixture_ref",
    "message_id",
    "sender",
    "subject",
    "sent_at",
    "mailbox",
    "raw_path",
    "parsed_headers_path",
    "parsed_message_path",
    "status",
    "created_at",
]

MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
DOC_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


@dataclass
class ImportRegistryStore:
    base_dir: str = "artifacts"
    relative_path: str = "state/import_registry.xlsx"

    @property
    def registry_path(self) -> Path:
        if self.base_dir == "artifacts" and self.relative_path == "state/import_registry.xlsx":
            return import_registry_path()
        return resolve_project_path(self.base_dir) / self.relative_path

    def append_or_get_existing(self, record: dict[str, Any]) -> tuple[dict[str, Any], bool, int]:
        rows = self.read_all()
        duplicate_index = self._find_duplicate_row_index(rows, record)
        if duplicate_index is not None:
            return rows[duplicate_index], False, duplicate_index + 2  # +1 header +1 indexing

        row = {header: str(record.get(header, "")) for header in REGISTRY_HEADERS}
        rows.append(row)
        self._write_rows(rows)
        return row, True, len(rows) + 1  # +1 header row

    def read_all(self) -> list[dict[str, str]]:
        path = self.registry_path
        if not path.exists():
            return []
        return self._read_rows(path)

    def get_max_imap_uid_for_mailbox(self, mailbox: str) -> int | None:
        rows = self.read_all()
        max_uid: int | None = None
        for row in rows:
            if row.get("source_mode", "") != "imap":
                continue
            if row.get("mailbox", "") != mailbox:
                continue
            raw_uid = str(row.get("uid", "")).strip()
            if not raw_uid.isdigit():
                continue
            uid = int(raw_uid)
            if max_uid is None or uid > max_uid:
                max_uid = uid
        return max_uid

    def _find_duplicate_row_index(self, rows: list[dict[str, str]], candidate: dict[str, Any]) -> int | None:
        mode = str(candidate.get("source_mode", ""))
        candidate_message_id = str(candidate.get("message_id", ""))

        for idx, row in enumerate(rows):
            if row.get("source_mode", "") != mode:
                continue
            if row.get("message_id", "") != candidate_message_id:
                continue

            if mode == "imap":
                if (
                    row.get("mailbox", "") == str(candidate.get("mailbox", ""))
                    and row.get("uid", "") == str(candidate.get("uid", ""))
                ):
                    return idx
            elif mode == "fixture":
                if row.get("fixture_ref", "") == str(candidate.get("fixture_ref", "")):
                    return idx
        return None

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

        all_rows: list[list[str]] = []
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
            all_rows.append(values)

        if not all_rows:
            return []

        headers = all_rows[0]
        result: list[dict[str, str]] = []
        for row_values in all_rows[1:]:
            padded = row_values + [""] * (len(headers) - len(row_values))
            result.append({headers[i]: padded[i] for i in range(len(headers))})
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
    <sheet name="imports" sheetId="1" r:id="rId1"/>
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
            "  <sheetData>",
        ]

        headers = REGISTRY_HEADERS
        lines.append(self._row_xml(1, headers))
        for idx, row in enumerate(rows, start=2):
            lines.append(self._row_xml(idx, [row.get(h, "") for h in headers]))

        lines.extend(["  </sheetData>", "</worksheet>"])
        return "\n".join(lines)

    @staticmethod
    def _row_xml(index: int, values: list[str]) -> str:
        cells = []
        for col_idx, value in enumerate(values, start=1):
            ref = f"{_col_name(col_idx)}{index}"
            escaped = _xml_escape(str(value))
            cells.append(f'    <c r="{ref}" t="inlineStr"><is><t>{escaped}</t></is></c>')
        return f'    <row r="{index}">\n' + "\n".join(cells) + "\n    </row>"

    @staticmethod
    def build_record(
        import_id: str,
        source_mode: str,
        uid: str,
        fixture_ref: str,
        message_id: str,
        sender: str,
        subject: str,
        sent_at: str,
        mailbox: str,
        raw_path: str,
        parsed_headers_path: str,
        parsed_message_path: str,
        status: str = "new",
    ) -> dict[str, str]:
        return {
            "import_id": import_id,
            "source_mode": source_mode,
            "uid": uid,
            "fixture_ref": fixture_ref,
            "message_id": message_id,
            "sender": sender,
            "subject": subject,
            "sent_at": sent_at,
            "mailbox": mailbox,
            "raw_path": raw_path,
            "parsed_headers_path": parsed_headers_path,
            "parsed_message_path": parsed_message_path,
            "status": status,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }


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
