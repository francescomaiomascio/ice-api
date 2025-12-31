from __future__ import annotations

from enum import Enum
from typing import Any, List, Optional


class PrimitiveType(str, Enum):
    """
    Tipo logico di un valore.
    NON è il tipo Python.
    È un'etichetta semantica condivisa.
    """

    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"

    PATH = "path"
    FILE = "file"
    DIRECTORY = "directory"

    JSON = "json"
    ANY = "any"

    CHOICE = "choice"


class ValueConstraint:
    """
    Vincoli opzionali per valori primitivi.
    Usati da validation / schema / GUI.
    """

    def __init__(
        self,
        *,
        choices: Optional[List[Any]] = None,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
    ):
        self.choices = choices
        self.min_value = min_value
        self.max_value = max_value
        self.min_length = min_length
        self.max_length = max_length
