from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.shared.common.paths import config_example_path, config_local_path


@dataclass
class LocalYamlConfigStore:
    path: str = "config.local.yaml"
    fallback_path: str | None = "config.example.yaml"

    def load(self) -> dict[str, Any]:
        local_path = config_local_path()
        example_path = config_example_path()

        if local_path.exists():
            return self._read_yaml(local_path)
        if example_path.exists():
            return self._read_yaml(example_path)

        raise FileNotFoundError(
            "Config file not found in project root. Checked: "
            f"{local_path}, {example_path}"
        )

    def get_section(self, section_name: str) -> dict[str, Any]:
        payload = self.load()
        section = payload.get(section_name, {})
        if not isinstance(section, dict):
            raise ValueError(f"Config section '{section_name}' must be an object")
        return section

    @staticmethod
    def _read_yaml(path: Path) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        current_root: str | None = None

        with path.open("r", encoding="utf-8") as f:
            for lineno, raw_line in enumerate(f, start=1):
                line = raw_line.rstrip()
                if not line.strip() or line.lstrip().startswith("#"):
                    continue

                indent = len(line) - len(line.lstrip(" "))
                content = line.strip()

                if indent == 0:
                    if not content.endswith(":"):
                        raise ValueError(f"Invalid root YAML at {path}:{lineno}")
                    current_root = content[:-1].strip()
                    payload[current_root] = {}
                    continue

                if indent < 2 or current_root is None:
                    raise ValueError(f"Invalid nested YAML at {path}:{lineno}")

                if ":" not in content:
                    raise ValueError(f"Invalid key/value YAML at {path}:{lineno}")

                key, value = content.split(":", 1)
                payload[current_root][key.strip()] = LocalYamlConfigStore._parse_scalar(value.strip())

        return payload

    @staticmethod
    def _parse_scalar(raw: str) -> Any:
        if "#" in raw and not raw.startswith(("'", '"')):
            raw = raw.split("#", 1)[0].strip()

        if raw == "":
            return ""
        if raw.lower() == "true":
            return True
        if raw.lower() == "false":
            return False
        if raw.lower() in {"null", "none"}:
            return None

        if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
            return raw[1:-1]

        if raw.startswith("[") and raw.endswith("]"):
            inner = raw[1:-1].strip()
            if not inner:
                return []
            return [LocalYamlConfigStore._parse_scalar(item.strip()) for item in inner.split(",")]

        if raw.isdigit() or (raw.startswith("-") and raw[1:].isdigit()):
            return int(raw)

        return raw
