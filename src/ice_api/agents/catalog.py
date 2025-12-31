from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Set

from ice_api.actions.base import ActionSpec
from ice_api.agents.spec import AgentSpec
from ice_api.types.enums import ActionDomain, ActionKind
from ice_api.types.identifiers import AgentName


# ============================================================================
# INTERNAL HELPERS
# ============================================================================

def _infer_main_domain(specs: List[ActionSpec]) -> ActionDomain:
    """
    Dominio principale = quello più frequente tra le azioni.
    """
    counts: Dict[ActionDomain, int] = {}
    for s in specs:
        counts[s.domain] = counts.get(s.domain, 0) + 1
    return max(counts, key=counts.get)


def _infer_capabilities(specs: List[ActionSpec]) -> List[str]:
    """
    Capability form: "<domain>:<kind>"
    Esempi:
        logs:analysis
        code:query
        workflow:plan
    """
    caps: Set[str] = set()
    for s in specs:
        caps.add(f"{s.domain.value}:{s.kind.value}")
    return sorted(caps)


def _infer_metadata(agent: AgentName, specs: List[ActionSpec]) -> dict:
    """
    Metadata utili per orchestrator e GUI.
    """
    return {
        "agent": agent,
        "action_count": len(specs),
        "domains": sorted({s.domain.value for s in specs}),
        "supports_mutation": any(s.kind == ActionKind.MUTATION for s in specs),
        "supports_analysis": any(s.kind == ActionKind.ANALYSIS for s in specs),
    }


def _default_description(agent: AgentName) -> str:
    """
    Descrizione fallback se non fornita altrove.
    """
    return f"Agent responsabile delle azioni '{agent}'"


# ============================================================================
# PUBLIC API
# ============================================================================

def build_agents_from_actions(
    actions: Iterable[ActionSpec],
) -> List[AgentSpec]:
    """
    Costruisce AgentSpec automaticamente a partire dalle ActionSpec.

    Fonte di verità:
        ActionSpec.owner_agent
    """

    by_agent: Dict[AgentName, List[ActionSpec]] = defaultdict(list)

    for action in actions:
        if action.owner_agent:
            by_agent[action.owner_agent].append(action)

    agents: List[AgentSpec] = []

    for agent_name, specs in sorted(by_agent.items()):
        agents.append(
            AgentSpec(
                name=agent_name,
                description=_default_description(agent_name),
                actions=[s.name for s in specs],
                capabilities=_infer_capabilities(specs),
                main_domain=_infer_main_domain(specs),
                metadata=_infer_metadata(agent_name, specs),
            )
        )

    return agents
