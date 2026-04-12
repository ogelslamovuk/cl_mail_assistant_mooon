from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class EmailHeaders:
    message_id: str
    in_reply_to: str | None = None
    references: list[str] = field(default_factory=list)
    subject: str = ""
    sender: str = ""
    sent_at: datetime | None = None
    to: list[str] = field(default_factory=list)
    cc: list[str] = field(default_factory=list)


@dataclass
class Message:
    message_id: str
    direction: str  # inbound | outbound
    headers: EmailHeaders
    body_text: str = ""
    raw_path: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Thread:
    thread_id: str
    message_ids: list[str] = field(default_factory=list)


@dataclass
class Case:
    case_id: str
    thread_id: str
    status: str = "new"
    history: list[str] = field(default_factory=list)


@dataclass
class RoutingDecision:
    route: str = "process"
    reason: str = ""


@dataclass
class DraftReply:
    subject: str = ""
    body: str = ""


@dataclass
class OperatorCard:
    case_id: str
    summary: str = ""


@dataclass
class OperatorAction:
    action: str = "approve"
    note: str = ""
