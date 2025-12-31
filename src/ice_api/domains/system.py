from __future__ import annotations

from typing import Dict, List

DOMAIN_NAME = "system"
DOMAIN_LABEL = "System"

DOMAIN_DESCRIPTION = (
    "Operazioni di sistema: workspace, filesystem, "
    "stato runtime e integrazioni di base."
)

DOMAIN_CAPABILITIES: List[str] = [
    "workspace",
    "filesystem",
    "status",
]

DOMAIN_UI_HINTS: Dict[str, str] = {
    "icon": "system",
    "color": "gray",
    "panel": "system",
}
