from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from src.shared.models.pipeline_context import PipelineContext


@dataclass
class ModuleResult:
    context: PipelineContext
    status: str = "ok"
    notes: list[str] = field(default_factory=list)
    artifact_refs: list[str] = field(default_factory=list)


class PipelineModule(Protocol):
    name: str

    def run(self, context: PipelineContext) -> ModuleResult:
        ...
