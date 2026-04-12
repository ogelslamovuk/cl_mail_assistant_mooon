from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ExcelStateStore:
    path: str
    _memory_state: dict = field(default_factory=dict)

    def read(self, key: str):
        return self._memory_state.get(key)

    def write(self, key: str, value):
        self._memory_state[key] = value
        return True
