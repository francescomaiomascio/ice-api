from __future__ import annotations

from typing import Dict, List

DOMAIN_NAME = "workflow"
DOMAIN_LABEL = "Workflow"

DOMAIN_DESCRIPTION = (
    "Pianificazione ed esecuzione di workflow multi-step, "
    "inclusa orchestrazione e valutazione del progresso."
)

DOMAIN_CAPABILITIES: List[str] = [
    "plan",
    "execute",
    "skip",
    "rollback",
    "evaluate",
]

DOMAIN_UI_HINTS: Dict[str, str] = {
    "icon": "workflow",
    "color": "purple",
    "panel": "workflow",
}
