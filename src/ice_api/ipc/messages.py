from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ice_api.types.enums import IPCMessageKind, ResultStatus
from ice_api.types.identifiers import (
    ActionName,
    WorkspaceId,
    SessionId,
    UserId,
)


# ============================================================================
# HEADER
# ============================================================================

@dataclass
class MessageHeader:
    """
    Header comune a TUTTI i messaggi IPC ICE.
    """

    kind: IPCMessageKind

    request_id: Optional[str] = None
    correlation_id: Optional[str] = None

    workspace_id: Optional[WorkspaceId] = None
    session_id: Optional[SessionId] = None
    user_id: Optional[UserId] = None

    source: str = "unknown"   # cli | gui | ide | agent | system


# ============================================================================
# ACTION REQUEST / RESPONSE
# ============================================================================

@dataclass
class ActionRequest:
    """
    Richiesta di esecuzione Action.
    """

    header: MessageHeader
    action: ActionName
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ActionError:
    """
    Errore strutturato, serializzabile.
    """

    code: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ActionResponse:
    """
    Risposta a una ActionRequest.
    """

    header: MessageHeader
    action: ActionName

    status: ResultStatus

    data: Any = None
    errors: List[ActionError] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

    def is_ok(self) -> bool:
        return self.status == ResultStatus.SUCCESS


# ============================================================================
# EVENTS
# ============================================================================

@dataclass
class EventMessage:
    """
    Evento asincrono (log, stato, progress, UI, ecc.)
    """

    header: MessageHeader
    event: str
    payload: Dict[str, Any] = field(default_factory=dict)
