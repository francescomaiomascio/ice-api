from __future__ import annotations

from typing import Dict, List

DOMAIN_NAME = "knowledge"
DOMAIN_LABEL = "Knowledge"

DOMAIN_DESCRIPTION = (
    "Knowledge base e RAG: ingest, indicizzazione, "
    "query semantiche e manutenzione."
)

DOMAIN_CAPABILITIES: List[str] = [
    "ingest",
    "index",
    "query",
    "search",
    "delete",
    "sync",
]

DOMAIN_UI_HINTS: Dict[str, str] = {
    "icon": "knowledge",
    "color": "teal",
    "panel": "knowledge",
}
