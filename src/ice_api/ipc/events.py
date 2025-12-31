from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from ice_api.types.enums import IPCMessageKind
from ice_api.types.identifiers import WorkspaceId, SessionId, UserId


@dataclass
class EventHeader:
    kind: IPCMessageKind = IPCMessageKind.EVENT

    event_id: Optional[str] = None
    correlation_id: Optional[str] = None

    workspace_id: Optional[WorkspaceId] = None
    session_id: Optional[SessionId] = None
    user_id: Optional[UserId] = None

    source: str = "system"


@dataclass
class EventMessage:
    header: EventHeader
    event: str
    payload: Dict[str, Any] = field(default_factory=dict)
