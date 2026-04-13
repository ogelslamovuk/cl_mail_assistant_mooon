from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def resolve_project_path(path_value: str | Path) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return (project_root() / path).resolve()


def artifacts_dir() -> Path:
    return resolve_project_path("artifacts")


def fixtures_dir() -> Path:
    return resolve_project_path("fixtures")


def config_local_path() -> Path:
    return resolve_project_path("config.local.yaml")


def config_example_path() -> Path:
    return resolve_project_path("config.example.yaml")


def import_registry_path() -> Path:
    return artifacts_dir() / "state" / "import_registry.xlsx"
