from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path
from typing import Callable, Dict, Any, Awaitable
import logging
import os
import time


logger = logging.getLogger("ice.api.ui.actions")

# =============================================================================
# DOCUMENTATION
# =============================================================================

DOCS_ROOT = Path(__file__).resolve().parents[3] / "docs"


def _list_docs_tree() -> list[dict]:
    tree = []
    for root, dirs, files in os.walk(DOCS_ROOT):
        rel = Path(root).relative_to(DOCS_ROOT)
        tree.append(
            {
                "path": str(rel),
                "dirs": dirs,
                "files": [f for f in files if f.endswith(".md")],
            }
        )
    return tree


def _load_doc(path: str) -> str:
    target = DOCS_ROOT / path
    if not target.exists():
        raise FileNotFoundError(f"Doc not found: {path}")
    return target.read_text(encoding="utf-8")


# =============================================================================
# ACTION REGISTRY
# =============================================================================

ACTIONS: Dict[str, Callable[..., Any]] = {}


def action(name: str):
    """
    Registra un'azione applicativa invocabile da qualunque interfaccia.
    """
    def decorator(fn):
        ACTIONS[name] = fn
        return fn
    return decorator


# =============================================================================
# DOCS ACTIONS
# =============================================================================

@action("docs.list")
def docs_list(_params: dict, _runtime):
    try:
        return {"ok": True, "docs": _list_docs_tree()}
    except Exception as exc:
        logger.exception("docs.list failed", exc_info=exc)
        return {"ok": False, "error": str(exc)}


@action("docs.read")
def docs_read(params: dict, _runtime):
    path = params.get("path")
    if not path:
        return {"ok": False, "error": "Missing document path"}
    try:
        return {"ok": True, "content": _load_doc(path)}
    except FileNotFoundError as exc:
        return {"ok": False, "error": str(exc)}
    except Exception as exc:
        logger.exception("docs.read failed", exc_info=exc, extra={"path": path})
        return {"ok": False, "error": "Unable to load document"}


# =============================================================================
# SYSTEM CHAT (STATEFUL, UI-AGNOSTIC)
# =============================================================================

_SYSTEM_CHAT_HISTORY = defaultdict(lambda: deque(maxlen=10))


def _get_system_agent(runtime):
    agent = None
    if hasattr(runtime, "get_agent"):
        try:
            agent = runtime.get_agent("system-agent")
        except Exception:
            agent = None
    if agent is None:
        system_service = getattr(runtime, "system_service", None)
        if system_service is not None:
            agent = getattr(system_service, "system_agent", None)
            if agent is None and hasattr(system_service, "get_agent"):
                try:
                    agent = system_service.get_agent("system-agent")
                except Exception:
                    agent = None
    if agent is None:
        raise RuntimeError("SystemAgent is not available on runtime")
    return agent


async def stream_system_chat(
    *,
    message: str,
    conversation_id: str,
    runtime,
    emit_event: Callable[[dict], Awaitable[None]],
    request_id: str | None = None,
):
    if not message:
        return

    if message == "__reset_memory__":
        _SYSTEM_CHAT_HISTORY.pop(conversation_id, None)
        await emit_event(
            {
                "type": "system.chat.stream",
                "event": "end",
                "conversation_id": conversation_id,
                "message_id": request_id,
                "full": "[System] Conversation reset.",
            }
        )
        return

    history = _SYSTEM_CHAT_HISTORY[conversation_id]

    messages = [{"role": "system", "content": "You are Cortex Studio System Assistant."}]
    for h in history:
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": h["assistant"]})
    messages.append({"role": "user", "content": message})

    agent = _get_system_agent(runtime)

    result = await agent.chat(
        ctx=None,
        user_message=message,
        history=messages,
    )

    full_text = result.payload.get("response") or ""
    history.append({"user": message, "assistant": full_text})

    tokens = full_text.split(" ")
    for i, tok in enumerate(tokens):
        await emit_event(
            {
                "type": "system.chat.stream",
                "event": "chunk",
                "conversation_id": conversation_id,
                "message_id": request_id,
                "delta": tok + (" " if i < len(tokens) - 1 else ""),
            }
        )

    await emit_event(
        {
            "type": "system.chat.stream",
            "event": "end",
            "conversation_id": conversation_id,
            "message_id": request_id,
            "full": full_text,
        }
    )


@action("system.chat.stream")
async def system_chat_stream(params: dict, runtime):
    """
    Placeholder: lo streaming reale viene gestito dal dispatcher
    che chiama stream_system_chat.
    """
    return {"ok": True}


# =============================================================================
# WORKSPACE ACTIONS
# =============================================================================

@action("workspace.list")
async def workspace_list(_params: dict, runtime):
    workspaces = runtime.session_manager.list_workspaces()
    return {
        "ok": True,
        "workspaces": [
            {"id": ws.workspace_id, "path": str(ws.base_path)}
            for ws in workspaces
        ],
    }


@action("workspace.create")
async def workspace_create(params: dict, runtime):
    name = params.get("name") or f"workspace-{int(time.time())}"
    description = params.get("description", "")
    tags = params.get("tags", [])
    ws_type = params.get("type", "multi_agent")

    try:
        ws = await runtime.session_manager.create_workspace(
            name=name,
            description=description,
            tags=tags,
            settings={"workspace_type": ws_type},
        )
        return {
            "ok": True,
            "workspace_id": ws.id,
            "name": ws.name,
            "root": str(ws.base_path),
            "workspace_type": ws.workspace_type,
            "backends": ws.list_backends(),
        }
    except Exception as exc:
        logger.exception("workspace.create failed", exc_info=exc)
        return {"ok": False, "error": str(exc)}


@action("workspace.load")
async def workspace_load(params: dict, runtime):
    wid = params.get("workspace_id")
    if not wid:
        return {"ok": False, "error": "Missing workspace_id"}

    ctx = await runtime.session_manager.activate_workspace(wid)
    ws = ctx.workspace

    return {
        "ok": True,
        "workspace_id": ws.id,
        "context_id": ctx.context_id,
        "workspace_type": ws.workspace_type,
        "project_root": str(ws.base_path),
    }


@action("workspace.unload")
async def workspace_unload(params: dict, runtime):
    wid = params.get("workspace_id")
    if not wid:
        return {"ok": False, "error": "Missing workspace_id"}
    await runtime.session_manager.deactivate_workspace(wid)
    return {"ok": True, "workspace_id": wid}


@action("workspace.delete")
async def workspace_delete(params: dict, runtime):
    wid = params.get("workspace_id")
    delete_from_disk = params.get("delete_from_disk", True)
    if not wid:
        return {"ok": False, "error": "Missing workspace_id"}
    await runtime.session_manager.delete_workspace(wid, delete_from_disk)
    return {"ok": True, "workspace_id": wid}


# =============================================================================
# CV PLUGIN
# =============================================================================

@action("cv.generate_json")
async def cv_generate_json(params: dict, runtime):
    return await runtime.get_agent("cv-agent").generate_json(**params)


@action("cv.ocr")
async def cv_ocr(params: dict, runtime):
    return await runtime.get_agent("cv-agent").ocr(params.get("paths", []))


@action("cv.render_html")
async def cv_render_html(params: dict, runtime):
    return await runtime.get_agent("cv-agent").render_html(params["cv_id"])


@action("cv.export_pdf")
async def cv_export_pdf(params: dict, runtime):
    return await runtime.get_agent("cv-agent").export_pdf(params["cv_id"])


@action("cv.cleanup")
async def cv_cleanup(params: dict, runtime):
    return await runtime.get_agent("cv-agent").cleanup(params["cv_id"])
