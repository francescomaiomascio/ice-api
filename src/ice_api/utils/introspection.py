from __future__ import annotations

from typing import Any, Dict, List

from ice_api.actions.base import ActionSpec
from ice_api.domains.base import Domain
from ice_api.ipc.messages import MessageSpec
from ice_api.lifecycle import LifecycleEvent


# ============================================================================
# DOMAIN INTROSPECTION
# ============================================================================

def describe_domain(domain: Domain) -> Dict[str, Any]:
    """
    Rappresentazione stabile di un Domain ICE-API.

    Usata da:
    - GUI (routing / panel binding)
    - IDE (hint semantici)
    """

    return {
        "name": domain.value,
        "description": domain.description,
        "ui_group": domain.ui_group,
    }


# ============================================================================
# ACTION INTROSPECTION
# ============================================================================

def describe_action(action: ActionSpec) -> Dict[str, Any]:
    """
    Rappresentazione completa e stabile di una ActionSpec ICE-API.

    NOTA:
    - owner_agent è una STRINGA
    - ICE-API non conosce AgentSpec
    """

    return {
        "name": action.name,
        "description": action.description,
        "domain": action.domain.value,
        "kind": action.kind.value,
        "version": action.version,
        "deprecated": action.deprecated,
        "tags": sorted(action.tags),
        "owner": action.owner,  # stringa logica (es: "planner-agent")
        "parameters": [
            {
                "name": p.name,
                "type": p.type.value,
                "required": p.required,
                "description": p.description,
                "default": p.default,
                "constraints": (
                    {
                        "min_value": p.constraints.min_value,
                        "max_value": p.constraints.max_value,
                        "min_length": p.constraints.min_length,
                        "max_length": p.constraints.max_length,
                        "choices": p.constraints.choices,
                    }
                    if p.constraints
                    else None
                ),
            }
            for p in action.parameters
        ],
        "result": [
            {
                "name": r.name,
                "type": r.type,
                "description": r.description,
                "required": r.required,
            }
            for r in action.result_fields
        ],
        "metadata": dict(action.metadata),
    }


# ============================================================================
# IPC MESSAGE INTROSPECTION
# ============================================================================

def describe_message(message: MessageSpec) -> Dict[str, Any]:
    """
    Descrizione formale di un messaggio IPC.
    """

    return {
        "name": message.name,
        "direction": message.direction.value,
        "payload_schema": message.payload_schema,
        "response_schema": message.response_schema,
        "version": message.version,
        "deprecated": message.deprecated,
    }


# ============================================================================
# LIFECYCLE INTROSPECTION
# ============================================================================

def describe_lifecycle_event(event: LifecycleEvent) -> Dict[str, Any]:
    """
    Evento lifecycle (boot, shutdown, workspace-open, ecc.)
    """

    return {
        "name": event.name,
        "description": event.description,
        "scope": event.scope,
    }


# ============================================================================
# API SNAPSHOT
# ============================================================================

def describe_api(
    *,
    domains: List[Domain],
    actions: List[ActionSpec],
    messages: List[MessageSpec],
    lifecycle_events: List[LifecycleEvent],
) -> Dict[str, Any]:
    """
    Snapshot completo dell'ICE-API.

    È IL CONTRATTO PUBBLICO del sistema.
    """

    return {
        "summary": {
            "total_domains": len(domains),
            "total_actions": len(actions),
            "total_messages": len(messages),
            "total_lifecycle_events": len(lifecycle_events),
        },
        "domains": {
            d.value: describe_domain(d)
            for d in domains
        },
        "actions": {
            a.name: describe_action(a)
            for a in actions
        },
        "ipc_messages": {
            m.name: describe_message(m)
            for m in messages
        },
        "lifecycle": {
            e.name: describe_lifecycle_event(e)
            for e in lifecycle_events
        },
    }