from __future__ import annotations

from typing import Any, Iterable, List

from ice_api.actions.base import ActionSpec, ParameterSpec
from ice_api.types.enums import ActionDomain, ActionKind
from ice_api.types.identifiers import ActionName, AgentName
from ice_api.types.primitives import PrimitiveType, ValueConstraint


# ============================================================================
# PARAMETER HELPERS
# ============================================================================

def _p(
    name: str,
    *,
    type: PrimitiveType = PrimitiveType.ANY,
    required: bool = False,
    description: str = "",
    default: Any = None,
    constraints: ValueConstraint | None = None,
) -> ParameterSpec:
    """
    Helper compatto per creare ParameterSpec coerenti con ice-api v1.

    - Nessun campo legacy (choices, min_value, ecc.)
    - Tutti i vincoli vivono in ValueConstraint
    """
    return ParameterSpec(
        name=name,
        type=type,
        required=required,
        description=description,
        default=default,
        constraints=constraints,
    )


# ============================================================================
# ACTION GROUPS (PER DOMINIO)
# ============================================================================

def build_logs_actions() -> List[ActionSpec]:
    return [
        ActionSpec(
            name="logs.scan",
            description="Scansiona una directory e individua le sorgenti di log.",
            domain=ActionDomain.LOGS,
            kind=ActionKind.ANALYSIS,
            parameters=[
                _p(
                    "path",
                    type=PrimitiveType.DIRECTORY,
                    required=True,
                    description="Directory contenente i file di log",
                ),
                _p(
                    "recursive",
                    type=PrimitiveType.BOOLEAN,
                    default=True,
                    description="Scansiona ricorsivamente le sottodirectory",
                ),
                _p(
                    "pattern",
                    type=PrimitiveType.STRING,
                    description="Pattern opzionale per filtrare i file",
                ),
            ],
            owner_agent="log-agent",
            tags=["logs", "scan"],
        ),
        ActionSpec(
            name="logs.tail",
            description="Legge le ultime N righe da un file di log.",
            domain=ActionDomain.LOGS,
            kind=ActionKind.QUERY,
            parameters=[
                _p(
                    "file",
                    type=PrimitiveType.FILE,
                    required=True,
                    description="File di log da leggere",
                ),
                _p(
                    "lines",
                    type=PrimitiveType.INTEGER,
                    default=100,
                    constraints=ValueConstraint(min_value=1),
                    description="Numero di righe da leggere",
                ),
                _p(
                    "follow",
                    type=PrimitiveType.BOOLEAN,
                    default=False,
                    description="Continua a seguire il file (tail -f)",
                ),
            ],
            owner_agent="log-agent",
            tags=["logs", "tail"],
        ),
    ]


def build_code_actions() -> List[ActionSpec]:
    return [
        ActionSpec(
            name="code.read_file",
            description="Legge il contenuto di un file di codice.",
            domain=ActionDomain.CODE,
            kind=ActionKind.QUERY,
            parameters=[
                _p(
                    "path",
                    type=PrimitiveType.FILE,
                    required=True,
                    description="Percorso del file di codice",
                ),
                _p(
                    "encoding",
                    type=PrimitiveType.STRING,
                    default="utf-8",
                    description="Encoding del file",
                ),
            ],
            owner_agent="code-agent",
            tags=["code", "read"],
        ),
        ActionSpec(
            name="code.explain",
            description="Spiega un frammento di codice.",
            domain=ActionDomain.CODE,
            kind=ActionKind.ANALYSIS,
            parameters=[
                _p(
                    "code",
                    type=PrimitiveType.STRING,
                    required=True,
                    description="Codice da spiegare",
                ),
                _p(
                    "language",
                    type=PrimitiveType.STRING,
                    description="Linguaggio di programmazione",
                ),
            ],
            owner_agent="code-agent",
            tags=["code", "explain"],
        ),
    ]


def build_workflow_actions() -> List[ActionSpec]:
    return [
        ActionSpec(
            name="workflow.plan",
            description="Genera un piano di workflow a partire da un obiettivo.",
            domain=ActionDomain.WORKFLOW,
            kind=ActionKind.PLAN,
            parameters=[
                _p(
                    "goal",
                    type=PrimitiveType.STRING,
                    required=True,
                    description="Obiettivo da pianificare",
                ),
            ],
            owner_agent="planner-agent",
            tags=["workflow", "plan"],
        ),
    ]


def build_system_actions() -> List[ActionSpec]:
    return [
        ActionSpec(
            name="system.workspace.list",
            description="Lista i workspace disponibili.",
            domain=ActionDomain.SYSTEM,
            kind=ActionKind.QUERY,
            owner_agent="system-agent",
            tags=["system", "workspace"],
        ),
    ]


# ============================================================================
# DEFAULT CATALOG
# ============================================================================

def build_default_actions() -> List[ActionSpec]:
    """
    Costruisce il catalogo completo delle ActionSpec ICE.

    QUESTA È LA FONTE DI VERITÀ PER:
    - orchestrator
    - CLI
    - GUI / IDE
    - LLM tools
    """
    actions: List[ActionSpec] = []

    actions.extend(build_logs_actions())
    actions.extend(build_code_actions())
    actions.extend(build_workflow_actions())
    actions.extend(build_system_actions())

    return actions


# ============================================================================
# UTILITIES
# ============================================================================

def action_names(actions: Iterable[ActionSpec]) -> List[ActionName]:
    """Restituisce la lista ordinata dei nomi azione."""
    return sorted(a.name for a in actions)
