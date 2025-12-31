from __future__ import annotations

from typing import Any, Dict, List

from ice_api.actions.base import ActionSpec, ParameterSpec, ResultFieldSpec
from ice_api.types.primitives import PrimitiveType


# ============================================================================
# PRIMITIVE → JSON SCHEMA TYPE
# ============================================================================

_PRIMITIVE_MAP: dict[PrimitiveType, Dict[str, Any]] = {
    PrimitiveType.STRING: {"type": "string"},
    PrimitiveType.INTEGER: {"type": "integer"},
    PrimitiveType.FLOAT: {"type": "number"},
    PrimitiveType.BOOLEAN: {"type": "boolean"},
    PrimitiveType.JSON: {"type": ["object", "array"]},
    PrimitiveType.PATH: {"type": "string"},
    PrimitiveType.FILE: {"type": "string"},
    PrimitiveType.DIRECTORY: {"type": "string"},
    PrimitiveType.ANY: {},
}


# ============================================================================
# PARAMETER → JSON SCHEMA
# ============================================================================

def parameter_to_jsonschema(p: ParameterSpec) -> Dict[str, Any]:
    schema: Dict[str, Any] = {}

    # base type
    schema.update(_PRIMITIVE_MAP.get(p.type, {}))

    # description
    if p.description:
        schema["description"] = p.description

    # default
    if p.default is not None:
        schema["default"] = p.default

    # choices
    if p.type == PrimitiveType.CHOICE and p.constraints:
        if p.constraints.choices:
            schema["enum"] = list(p.constraints.choices)

    # numeric constraints
    if p.constraints:
        if p.constraints.min_value is not None:
            schema["minimum"] = p.constraints.min_value
        if p.constraints.max_value is not None:
            schema["maximum"] = p.constraints.max_value

        if p.constraints.min_length is not None:
            schema["minLength"] = p.constraints.min_length
        if p.constraints.max_length is not None:
            schema["maxLength"] = p.constraints.max_length

    return schema


# ============================================================================
# RESULT FIELD → JSON SCHEMA (SOFT)
# ============================================================================

def result_field_to_jsonschema(r: ResultFieldSpec) -> Dict[str, Any]:
    """
    Risultato volutamente soft:
    - non imponiamo struttura rigida
    - utile per docs / LLM
    """
    return {
        "type": "object",
        "description": r.description or r.type,
    }


# ============================================================================
# ACTION → JSON SCHEMA
# ============================================================================

def action_to_jsonschema(action: ActionSpec) -> Dict[str, Any]:
    """
    Genera JSON Schema completo per una ActionSpec.
    """

    properties: Dict[str, Any] = {}
    required: List[str] = []

    for p in action.parameters:
        properties[p.name] = parameter_to_jsonschema(p)
        if p.required:
            required.append(p.name)

    schema: Dict[str, Any] = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": action.name,
        "description": action.description,
        "type": "object",
        "properties": properties,
        "additionalProperties": True,
    }

    if required:
        schema["required"] = required

    return schema


# ============================================================================
# METADATA WRAPPER (per GUI / IDE / LLM)
# ============================================================================

def action_schema_bundle(action: ActionSpec) -> Dict[str, Any]:
    """
    Bundle completo:
    - input schema
    - output hints
    - metadata semantica
    """
    return {
        "name": action.name,
        "domain": action.domain.value,
        "kind": action.kind.value,
        "version": action.version,
        "deprecated": action.deprecated,
        "tags": action.tags,
        "owner_agent": action.owner_agent,
        "input_schema": action_to_jsonschema(action),
        "result_fields": [
            {
                "name": r.name,
                "type": r.type,
                "description": r.description,
                "required": r.required,
            }
            for r in action.result_fields
        ],
        "metadata": action.metadata,
    }
