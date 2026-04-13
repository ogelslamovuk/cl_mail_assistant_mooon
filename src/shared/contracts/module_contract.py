from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from typing import Protocol

from src.shared.models.pipeline_context import PipelineContext


@dataclass
class ModuleResult:
    context: PipelineContext
    status: str = "ok"
    notes: list[str] = field(default_factory=list)
    artifact_refs: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)


class PipelineModule(Protocol):
    name: str

    def run(self, context: PipelineContext) -> ModuleResult:
        ...
