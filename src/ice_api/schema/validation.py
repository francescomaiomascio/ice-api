from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from ice_api.actions.base import ActionSpec, ParameterSpec
from ice_api.types.primitives import PrimitiveType, ValueConstraint
from ice_api.ipc.errors import InvalidParametersError


# ============================================================================
# VALIDATION STRUCTURES
# ============================================================================

@dataclass
class ValidationIssue:
    param: str
    message: str


@dataclass
class ValidationResult:
    ok: bool
    issues: List[ValidationIssue] = field(default_factory=list)

    def raise_if_error(self, *, action_name: str) -> None:
        """
        Solleva InvalidParametersError se la validazione non è OK.
        """
        if not self.ok:
            errors = {iss.param: iss.message for iss in self.issues}
            raise InvalidParametersError(action=action_name, errors=errors)


# ============================================================================
# SINGLE PARAM VALIDATION
# ============================================================================

def _validate_type(value: Any, ptype: PrimitiveType) -> bool:
    """
    Type check SOFT, non coercitivo.
    """
    if ptype == PrimitiveType.STRING:
        return isinstance(value, str)

    if ptype == PrimitiveType.INTEGER:
        return isinstance(value, int)

    if ptype == PrimitiveType.FLOAT:
        return isinstance(value, (int, float))

    if ptype == PrimitiveType.BOOLEAN:
        return isinstance(value, bool)

    if ptype == PrimitiveType.JSON:
        return isinstance(value, (dict, list))

    if ptype in {PrimitiveType.PATH, PrimitiveType.FILE, PrimitiveType.DIRECTORY}:
        # Path validation vera avverrà altrove (engine / system)
        return isinstance(value, (str, bytes)) or hasattr(value, "__fspath__")

    if ptype == PrimitiveType.CHOICE:
        return True  # check fatto nei constraint

    return True  # ANY


def _validate_constraints(
    value: Any,
    constraint: ValueConstraint,
) -> List[str]:
    """
    Valida min/max/value constraints.
    """
    issues: List[str] = []

    if value is None:
        return issues

    if isinstance(value, (int, float)):
        if constraint.min_value is not None and value < constraint.min_value:
            issues.append(f"valore < min_value ({constraint.min_value})")
        if constraint.max_value is not None and value > constraint.max_value:
            issues.append(f"valore > max_value ({constraint.max_value})")

    if isinstance(value, str):
        if constraint.min_length is not None and len(value) < constraint.min_length:
            issues.append(f"lunghezza < min_length ({constraint.min_length})")
        if constraint.max_length is not None and len(value) > constraint.max_length:
            issues.append(f"lunghezza > max_length ({constraint.max_length})")

    if constraint.choices is not None:
        if value not in constraint.choices:
            issues.append(f"valore non ammesso, consentiti: {constraint.choices}")

    return issues


def _validate_param(
    param: ParameterSpec,
    value: Any,
) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []

    # missing required
    if value is None:
        if param.required and param.default is None:
            issues.append(
                ValidationIssue(
                    param=param.name,
                    message="Parametro richiesto ma non fornito",
                )
            )
        return issues

    # type check
    if not _validate_type(value, param.type):
        issues.append(
            ValidationIssue(
                param=param.name,
                message=f"Tipo non valido (atteso {param.type.value})",
            )
        )
        return issues

    # constraints
    if param.constraints:
        msgs = _validate_constraints(value, param.constraints)
        for msg in msgs:
            issues.append(
                ValidationIssue(
                    param=param.name,
                    message=msg,
                )
            )

    return issues


# ============================================================================
# ACTION VALIDATION
# ============================================================================

def validate_params(
    action: ActionSpec,
    params: Dict[str, Any],
) -> ValidationResult:
    """
    Valida parametri runtime contro ActionSpec.

    NON:
    - fa coercion
    - accede al filesystem
    - lancia eccezioni direttamente
    """
    issues: List[ValidationIssue] = []

    declared_params = {p.name: p for p in action.parameters}

    # 1. parametri dichiarati
    for name, spec in declared_params.items():
        value = params.get(name, spec.default)
        issues.extend(_validate_param(spec, value))

    # 2. parametri sconosciuti
    if declared_params:
        for key in params.keys():
            if key not in declared_params:
                issues.append(
                    ValidationIssue(
                        param=key,
                        message="Parametro non riconosciuto dall'azione",
                    )
                )

    return ValidationResult(ok=not issues, issues=issues)
