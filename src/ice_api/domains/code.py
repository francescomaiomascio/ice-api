from __future__ import annotations

from typing import Dict, List

DOMAIN_NAME = "code"
DOMAIN_LABEL = "Code"

DOMAIN_DESCRIPTION = (
    "Analisi e manipolazione del codice sorgente: "
    "lettura file, AST, simboli, refactor e code intelligence."
)

DOMAIN_CAPABILITIES: List[str] = [
    "read",
    "analyze",
    "search",
    "rewrite",
    "refactor",
    "generate",
]

DOMAIN_UI_HINTS: Dict[str, str] = {
    "icon": "code",
    "color": "blue",
    "panel": "code",
}
