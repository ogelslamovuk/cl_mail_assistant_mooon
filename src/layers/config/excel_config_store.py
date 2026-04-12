from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ExcelConfigStore:
    path: str

    def load(self) -> dict:
        # Skeleton placeholder: Excel parsing will be implemented in later stages.
        return {"source": str(Path(self.path)), "format": "excel", "loaded": True}
