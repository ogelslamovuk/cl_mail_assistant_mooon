from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .entities import Case, DraftReply, Message, OperatorAction, OperatorCard, RoutingDecision, Thread


@dataclass
class PipelineContext:
    run_id: str
    message: Message | None = None
    thread: Thread | None = None
    case: Case | None = None
    enrichment: dict[str, Any] = field(default_factory=dict)
    understanding: dict[str, Any] = field(default_factory=dict)
    routing: RoutingDecision | None = None
    draft: DraftReply | None = None
    operator_card: OperatorCard | None = None
    operator_action: OperatorAction | None = None
    artifacts: dict[str, list[str]] = field(default_factory=dict)
