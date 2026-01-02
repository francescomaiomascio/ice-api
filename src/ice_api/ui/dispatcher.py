from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, Callable, Awaitable

from ice_api.ipc.errors import WorkspaceNotFoundError
from ice_api.ui.actions import ACTIONS, stream_system_chat
from ice_api.ui.context import SessionContext

logger = logging.getLogger("ice.api.ui.dispatcher")

# ============================================================================
# ACTIONS THAT DO NOT REQUIRE AN ACTIVE WORKSPACE
# ============================================================================

NO_WORKSPACE_REQUIRED = {
    "workspace.create",
    "workspace.delete",
    "workspace.unload",
    "workspace.list",
    "system.chat.stream",
    "cv.generate_json",
    "cv.ocr",
    "cv.render_html",
    "cv.export_pdf",
    "cv.cleanup",
}

# ============================================================================
# MAIN DISPATCH ENTRYPOINT
# ============================================================================

async def dispatch(
    request: dict,
    runtime,
    *,
    emit_event: Callable[[dict], Awaitable[None]] | None = None,
) -> dict | None:
    """
    Dispatches an API/UI request to the appropriate action.

    - request: normalized request dict
    - runtime: active ICE runtime
    - emit_event: optional async event emitter (WS, SSE, etc.)
    """

    action_name = request.get("action") or request.get("method")
    params = request.get("params", {}) or {}
    request_id = request.get("id")

    logger.debug("DISPATCH_REQUEST", extra={"action": action_name})

    # ---------------------------------------------------------------------
    # STREAMING SYSTEM CHAT (SPECIAL CASE)
    # ---------------------------------------------------------------------

    if action_name == "system.chat.stream":
        if not emit_event:
            return {"ok": False, "error": "Streaming requires emit_event"}

        conversation_id = params.get("conversation_id") or "default"
        message = (params.get("message") or "").strip()

        ctx = SessionContext.current()
        if ctx and request_id:
            setattr(ctx, "request_id", request_id)

        await stream_system_chat(
            message=message,
            conversation_id=conversation_id,
            runtime=runtime,
            emit_event=emit_event,
            request_id=request_id,
        )
        return None

    # ---------------------------------------------------------------------
    # ACTION LOOKUP
    # ---------------------------------------------------------------------

    action = ACTIONS.get(action_name)
    if not action:
        logger.error("Unknown action requested", extra={"action": action_name})
        return {"ok": False, "error": f"Unknown action: {action_name}"}

    # ---------------------------------------------------------------------
    # WORKSPACE CONTEXT RESOLUTION
    # ---------------------------------------------------------------------

    workspace_id = (
        request.get("workspace_id")
        or params.get("workspace_id")
        or runtime.session_manager.current_workspace_id
    )

    requires_workspace = action_name not in NO_WORKSPACE_REQUIRED
    current_ctx = SessionContext.current()

    if requires_workspace and not workspace_id:
        return {"ok": False, "error": "Missing workspace_id"}

    if requires_workspace:
        if not current_ctx or current_ctx.workspace_id != workspace_id:
            try:
                current_ctx = await runtime.session_manager.activate_workspace(workspace_id)
            except Exception as exc:
                if not isinstance(exc, WorkspaceNotFoundError):
                    exc = WorkspaceNotFoundError(workspace_id)
                logger.error(
                    "Workspace activation failed",
                    exc_info=True,
                    extra={"workspace_id": workspace_id},
                )
                return {"ok": False, "error": str(exc)}

    # Optional panel / UI context (still abstract)
    panel_context = request.get("panel_context") or params.get("panel_context")
    if panel_context and current_ctx:
        current_ctx.set_panel_context(panel_context)

    # ---------------------------------------------------------------------
    # ACTION EXECUTION
    # ---------------------------------------------------------------------

    try:
        result = action(params, runtime)
        if asyncio.iscoroutine(result):
            result = await result

        if emit_event and isinstance(result, dict) and result.get("ok"):
            await _emit_post_action_events(
                action_name=action_name,
                result=result,
                runtime=runtime,
                emit_event=emit_event,
                fallback_workspace_id=workspace_id,
            )

        return result

    except Exception as exc:
        logger.exception(
            "Action execution failed",
            extra={"action": action_name, "workspace_id": workspace_id},
        )
        return {"ok": False, "error": str(exc)}

# ============================================================================
# POST-ACTION EVENTS
# ============================================================================

async def _emit_post_action_events(
    *,
    action_name: str,
    result: dict,
    runtime,
    emit_event: Callable[[dict], Awaitable[None]],
    fallback_workspace_id: str | None,
):
    """
    Emits standard lifecycle events after certain actions.
    """

    if action_name in {"workspace.create", "workspace.load"}:
        await _emit_workspace_loaded(runtime, result, emit_event)

    if action_name in {"workspace.create", "workspace.delete"}:
        wid = (
            result.get("workspace_id")
            or result.get("workspace")
            or fallback_workspace_id
        )
        await emit_event(
            {
                "event": "workspace.list.updated",
                "workspace_id": wid,
            }
        )


async def _emit_workspace_loaded(runtime, result: dict, emit_event):
    workspace_id = result.get("workspace_id") or result.get("workspace")
    if not workspace_id:
        return

    try:
        ws = runtime.session_manager.get_workspace(workspace_id)
    except Exception:
        return

    ai_config = getattr(ws, "ai_config", {}) or {}
    if hasattr(ai_config, "to_dict"):
        try:
            ai_config = ai_config.to_dict()
        except Exception:
            ai_config = {}

    payload = {
        "event": "workspace.loaded",
        "workspace": {
            "workspace_id": workspace_id,
            "name": getattr(ws, "name", workspace_id),
            "type": getattr(ws, "workspace_type", "generic"),
            "project_root": str(getattr(ws, "base_path", "")),
            "features": {
                "kg_enabled": bool(ai_config.get("kg", {}).get("enabled")),
                "rag_enabled": bool(ai_config.get("rag", {}).get("enabled")),
            },
        },
    }

    logger.info(
        "EVENT workspace.loaded emitted",
        extra={"workspace_id": workspace_id},
    )
    await emit_event(payload)
