from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from ice_api.types.enums import ActionDomain
from ice_api.types.identifiers import ActionName, AgentName


# ============================================================================
# AGENT SPEC
# ============================================================================

@dataclass
class AgentSpec:
    """
    Contratto dichiarativo di un Agent ICE.

    Serve a:
    - orchestrator (routing, scheduling)
    - CLI (help, list, inspect)
    - GUI / IDE (visualizzazione capacità)
    - introspection / schema

    NON contiene implementazione.
    """

    # identificazione
    name: AgentName
    description: str

    # azioni di cui è owner
    actions: List[ActionName] = field(default_factory=list)

    # capabilities semantiche ad alto livello
    # es: ["logs:analysis", "code:mutation", "workflow:plan"]
    capabilities: List[str] = field(default_factory=list)

    # dominio principale (per grouping UI)
    main_domain: ActionDomain = ActionDomain.OTHER

    # metadata liberi (UI, orchestrator, future use)
    metadata: Dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # helpers (safe)
    # ------------------------------------------------------------------

    def owns_action(self, action_name: ActionName) -> bool:
        """True se l'agente è owner dell'azione."""
        return action_name in self.actions
