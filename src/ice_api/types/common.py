from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ice_api.types.enums import ResultStatus
from ice_api.types.identifiers import (
    ActionName,
    WorkspaceId,
    SessionId,
    UserId,
)


# ============================================================================
# ACTION CONTEXT
# ============================================================================

@dataclass
class ActionContext:
    """
    Contesto logico di esecuzione di una Action.

    NON è trasporto.
    NON è runtime.
    È semantica condivisa.
    """

    workspace_id: Optional[WorkspaceId] = None
    session_id: Optional[SessionId] = None
    user_id: Optional[UserId] = None

    source: str = "unknown"   # cli | gui | ide | agent | system

    panel_context: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# ACTION CALL
# ============================================================================

@dataclass
class ActionCall:
    """
    Rappresentazione logica di una richiesta Action.

    Usata da:
    - Engine
    - Orchestrator
    - Agents
    """

    name: ActionName
    params: Dict[str, Any] = field(default_factory=dict)
    context: ActionContext = field(default_factory=ActionContext)

    request_id: Optional[str] = None


# ============================================================================
# ACTION RESULT
# ============================================================================

@dataclass
class ActionError:
    """
    Errore logico di una Action (non eccezione Python).
    """

    code: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ActionResult:
    """
    Risultato logico di una ActionCall.

    NON contiene riferimenti a IPC, network o runtime.
    """

    name: ActionName
    status: ResultStatus

    data: Any = None
    errors: List[ActionError] = field(default_factory=list)

    metrics: Dict[str, Any] = field(default_factory=dict)
    context: Optional[ActionContext] = None

    def is_ok(self) -> bool:
        return self.status == ResultStatus.SUCCESS

    def add_error(self, code: str, message: str, **details: Any) -> None:
        self.errors.append(
            ActionError(code=code, message=message, details=details)
        )
        if self.status == ResultStatus.SUCCESS:
            self.status = ResultStatus.FAILED
