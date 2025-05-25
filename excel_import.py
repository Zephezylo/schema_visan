import re
import zipfile
import xml.etree.ElementTree as ET
from typing import List, Dict

from models import Parent

NS = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def _column_index(col: str) -> int:
    """Convert Excel column letters to zero-based index."""
    index = 0
    for ch in col:
        if not ch.isalpha():
            break
        index = index * 26 + (ord(ch.upper()) - 64)
    return index - 1


def _parse_xlsx(path: str) -> List[Dict[str, str]]:
    """Parse first sheet of an XLSX file into a list of row dicts."""
    with zipfile.ZipFile(path) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            tree = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for t in tree.findall(".//main:t", NS):
                shared.append(t.text or "")

        sheet_name = "xl/worksheets/sheet1.xml"
        tree = ET.fromstring(z.read(sheet_name))

        rows = []
        for row in tree.findall(".//main:sheetData/main:row", NS):
            cells = {}
            for c in row.findall("main:c", NS):
                ref = c.attrib.get("r", "")
                col_letters = re.match(r"[A-Z]+", ref).group()
                idx = _column_index(col_letters)

                value = ""
                v = c.find("main:v", NS)
                if v is not None:
                    if c.attrib.get("t") == "s":
                        value = shared[int(v.text)]
                    else:
                        value = v.text
                cells[idx] = value
            if cells:
                rows.append(cells)

        if not rows:
            return []

        # Normalize rows to list of dicts using header row
        header_cells = rows[0]
        max_idx = max(header_cells.keys())
        header = [header_cells.get(i, "") for i in range(max_idx + 1)]
        result = []
        for row_cells in rows[1:]:
            values = [row_cells.get(i, "") for i in range(max_idx + 1)]
            result.append({header[i]: values[i] for i in range(len(header))})
        return result


def load_parents_from_excel(path: str) -> List[Parent]:
    """Load Parent objects from an Excel file."""
    rows = _parse_xlsx(path)
    parents: List[Parent] = []
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for row in rows:
        if not row.get("Name"):
            continue
        prefs = {}
        for day in weekdays:
            val = row.get(day)
            if val:
                try:
                    prefs[day] = int(float(val))
                except ValueError:
                    pass
        quota = 0
        if row.get("Quota"):
            try:
                quota = int(float(row["Quota"]))
            except ValueError:
                quota = 0
        parents.append(Parent(name=row["Name"], quota=quota, preferences=prefs))
    return parents
