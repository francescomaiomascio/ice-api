from __future__ import annotations

from typing import Dict, List

DOMAIN_NAME = "workspace"
DOMAIN_LABEL = "Workspace"

DOMAIN_DESCRIPTION = (
    "Ispezione e gestione dei workspace: configurazione, "
    "backends, statistiche e contesto globale."
)

DOMAIN_CAPABILITIES: List[str] = [
    "inspect",
    "switch",
    "stats",
]

DOMAIN_UI_HINTS: Dict[str, str] = {
    "icon": "workspace",
    "color": "green",
    "panel": "workspace",
}
