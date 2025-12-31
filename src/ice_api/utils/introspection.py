from __future__ import annotations

from typing import Any, Dict, List

from ice_api.actions.base import ActionSpec
from ice_api.agents.spec import AgentSpec


# ============================================================================
# ACTION INTROSPECTION
# ============================================================================

def describe_action(action: ActionSpec) -> Dict[str, Any]:
    """
    Rappresentazione completa e stabile di una ActionSpec.

    Usata da:
    - GUI (form, pannelli)
    - CLI (help)
    - IDE (completions)
    - LLM (tool description)
    """

    return {
        "name": action.name,
        "description": action.description,
        "domain": action.domain.value,
        "kind": action.kind.value,
        "version": action.version,
        "deprecated": action.deprecated,
        "tags": list(action.tags),
        "owner_agent": action.owner_agent,
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
# AGENT INTROSPECTION
# ============================================================================

def describe_agent(agent: AgentSpec) -> Dict[str, Any]:
    """
    Rappresentazione completa di un AgentSpec.
    """

    return {
        "name": agent.name,
        "description": agent.description,
        "main_domain": agent.main_domain.value,
        "actions": list(agent.actions),
        "capabilities": list(agent.capabilities),
        "metadata": dict(agent.metadata),
    }


# ============================================================================
# CATALOG INTROSPECTION
# ============================================================================

def describe_catalog(
    *,
    actions: List[ActionSpec],
    agents: List[AgentSpec],
) -> Dict[str, Any]:
    """
    Snapshot completo dell'API ICE.

    È IL PAYLOAD che:
    - la GUI carica all’avvio
    - l’IDE usa per suggestion
    - la CLI usa per help
    - l’LLM usa per tool discovery
    """

    by_domain: Dict[str, List[str]] = {}
    for action in actions:
        by_domain.setdefault(action.domain.value, []).append(action.name)

    # ordering deterministico
    for domain in by_domain:
        by_domain[domain].sort()

    return {
        "summary": {
            "total_actions": len(actions),
            "total_agents": len(agents),
            "domains": sorted(by_domain.keys()),
        },
        "index": {
            "by_domain": by_domain,
            "by_agent": {
                agent.name: sorted(agent.actions)
                for agent in agents
            },
        },
        "actions": {
            action.name: describe_action(action)
            for action in actions
        },
        "agents": {
            agent.name: describe_agent(agent)
            for agent in agents
        },
    }
