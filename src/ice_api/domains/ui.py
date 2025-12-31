from __future__ import annotations

from typing import Dict, List

DOMAIN_NAME = "ui"
DOMAIN_LABEL = "UI"

DOMAIN_DESCRIPTION = (
    "Azioni di supporto all'interfaccia utente: "
    "tracking pannelli, preview, stub UI."
)

DOMAIN_CAPABILITIES: List[str] = [
    "panel",
    "preview",
    "tracking",
]

DOMAIN_UI_HINTS: Dict[str, str] = {
    "icon": "ui",
    "color": "pink",
    "panel": "ui",
}
