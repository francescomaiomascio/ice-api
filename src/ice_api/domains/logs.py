from __future__ import annotations

from typing import Dict, List

DOMAIN_NAME = "logs"
DOMAIN_LABEL = "Logs"

DOMAIN_DESCRIPTION = (
    "Gestione e analisi dei log: scansione file, parsing, "
    "normalizzazione, ricerca e indicizzazione."
)

DOMAIN_CAPABILITIES: List[str] = [
    "scan",
    "read",
    "tail",
    "parse",
    "normalize",
    "filter",
    "search",
    "index",
]

DOMAIN_UI_HINTS: Dict[str, str] = {
    "icon": "logs",
    "color": "orange",
    "panel": "logs",
}
