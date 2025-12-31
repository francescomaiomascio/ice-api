from __future__ import annotations

from ice_api.version import __version__

# Core contracts
from ice_api.actions.base import ActionSpec, ParameterSpec, ResultFieldSpec
from ice_api.agents.spec import AgentSpec

# Catalog builders
from ice_api.actions.catalog import build_default_actions
from ice_api.agents.catalog import build_agents_from_actions

# IPC
from ice_api.ipc.messages import (
    MessageHeader,
    ActionRequest,
    ActionResponse,
    EventMessage,
)

# Types
from ice_api.types.enums import (
    ActionDomain,
    ActionKind,
    LifecyclePhase,
    IPCMessageKind,
    ResultStatus,
)

from ice_api.types.identifiers import (
    ActionName,
    AgentName,
    WorkspaceId,
    SessionId,
    UserId,
)

__all__ = [
    "__version__",
    # specs
    "ActionSpec",
    "ParameterSpec",
    "ResultFieldSpec",
    "AgentSpec",
    # builders
    "build_default_actions",
    "build_agents_from_actions",
    # ipc
    "MessageHeader",
    "ActionRequest",
    "ActionResponse",
    "EventMessage",
    # enums
    "ActionDomain",
    "ActionKind",
    "LifecyclePhase",
    "IPCMessageKind",
    "ResultStatus",
    # identifiers
    "ActionName",
    "AgentName",
    "WorkspaceId",
    "SessionId",
    "UserId",
]
