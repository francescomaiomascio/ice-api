from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ice_api.types.enums import ActionDomain, ActionKind
from ice_api.types.identifiers import ActionName, AgentName
from ice_api.types.primitives import PrimitiveType, ValueConstraint


# ============================================================================
# PARAMETER SPEC
# ============================================================================

@dataclass
class ParameterSpec:
    """
    Specifica dichiarativa di un parametro di input per una Action.

    È un CONTRATTO:
    - CLI (help, parsing)
    - GUI (form dinamici)
    - LLM tools (JSON schema)
    - Validation

    NON contiene logica.
    """

    name: str
    type: PrimitiveType = PrimitiveType.ANY

    required: bool = False
    description: str = ""
    default: Any = None

    constraints: Optional[ValueConstraint] = None


# ============================================================================
# RESULT FIELD SPEC
# ============================================================================

@dataclass
class ResultFieldSpec:
    """
    Descrizione semantica di un campo nel risultato di un'Action.

    NON è un JSON Schema completo.
    Serve come guida per:
    - CLI
    - GUI
    - LLM
    """

    name: str
    description: str = ""
    type: str = "any"   # es: "list[LogEvent]", "dict", "WorkflowPlan"
    required: bool = False


# ============================================================================
# ACTION SPEC
# ============================================================================

@dataclass
class ActionSpec:
    """
    Contratto dichiarativo di una Action ICE.

    È la FONTE DI VERITÀ per:
    - engine
    - orchestrator
    - IPC
    - CLI / GUI / IDE
    - LLM routing

    NON contiene implementazione.
    """

    # identificazione
    name: ActionName
    description: str

    # semantica
    domain: ActionDomain
    kind: ActionKind

    # input
    parameters: List[ParameterSpec] = field(default_factory=list)

    # output
    result_fields: List[ResultFieldSpec] = field(default_factory=list)

    # ownership
    owner_agent: Optional[AgentName] = None

    # metadata / docs / routing
    tags: List[str] = field(default_factory=list)
    deprecated: bool = False
    version: str = "v1"

    metadata: Dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # helpers (safe, non-runtime)
    # ------------------------------------------------------------------

    def get_param(self, name: str) -> Optional[ParameterSpec]:
        """Restituisce un ParameterSpec per nome, se esiste."""
        for p in self.parameters:
            if p.name == name:
                return p
        return None
