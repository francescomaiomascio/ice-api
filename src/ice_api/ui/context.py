# ice_api/ui/context.py

from __future__ import annotations

from contextvars import ContextVar
from typing import Optional


class UIContext:
    """
    UI-scoped contextual information.
    This is NOT a runtime/session context.
    """

    def __init__(self) -> None:
        self.request_id: str | None = None
        self.panel_context: str | None = None

    def set_panel_context(self, panel: str) -> None:
        self.panel_context = panel


_current_context: ContextVar[Optional["SessionContext"]] = ContextVar(
    "ice_api_ui_session_context",
    default=None,
)


class SessionContext:
    """
    Lightweight, runtime-agnostic session context for UI dispatch.
    """

    def __init__(self, *, workspace_id: str | None = None) -> None:
        self.workspace_id = workspace_id
        self.request_id: str | None = None
        self.panel_context: str | None = None

    def set_panel_context(self, panel: str) -> None:
        self.panel_context = panel

    @classmethod
    def current(cls) -> Optional["SessionContext"]:
        return _current_context.get()

    @classmethod
    def set_current(cls, context: Optional["SessionContext"]) -> None:
        _current_context.set(context)
