from __future__ import annotations

from typing import Any, Dict, Optional


# ============================================================================
# BASE IPC / API ERROR
# ============================================================================

class ApiError(Exception):
    """
    Errore base dell'API ICE.

    È:
    - serializzabile
    - trasportabile via IPC
    - consumabile da CLI / GUI / LLM
    """

    code: str = "api.error"

    def __init__(self, message: str, *, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


class IPCError(ApiError):
    """
    Alias semantico di ApiError per il layer IPC.

    Serve per:
    - chiarezza concettuale
    - backward compatibility
    - import stabili da ice_api.ipc
    """
    pass


# ============================================================================
# LOOKUP ERRORS
# ============================================================================

class ActionNotFoundError(ApiError):
    code = "api.action.not_found"

    def __init__(self, action: str):
        super().__init__(
            f"Azione '{action}' non trovata.",
            details={"action": action},
        )


class AgentNotFoundError(ApiError):
    code = "api.agent.not_found"

    def __init__(self, agent: str):
        super().__init__(
            f"Agente '{agent}' non trovato.",
            details={"agent": agent},
        )


# ============================================================================
# VALIDATION ERRORS
# ============================================================================

class InvalidParametersError(ApiError):
    code = "api.params.invalid"

    def __init__(self, action: str, errors: Dict[str, str]):
        super().__init__(
            f"Parametri non validi per '{action}'.",
            details={"action": action, "errors": errors},
        )


class IPCValidationError(InvalidParametersError):
    """
    Errore di validazione a livello IPC.

    Alias semantico di InvalidParametersError
    per distinguere:
    - validazione API
    - validazione IPC / payload
    """
    pass


# ============================================================================
# EXECUTION / ROUTING ERRORS
# ============================================================================

class ActionExecutionError(ApiError):
    code = "api.action.execution"

    def __init__(
        self,
        action: str,
        *,
        agent: str,
        exception: Exception,
        partial_result: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            f"Errore durante l'esecuzione di '{action}' da parte di '{agent}'.",
            details={
                "action": action,
                "agent": agent,
                "exception_type": type(exception).__name__,
                "exception_message": str(exception),
                "partial_result": partial_result,
            },
        )


class OrchestratorRoutingError(ApiError):
    code = "api.orchestrator.routing"

    def __init__(self, action: str):
        super().__init__(
            f"Impossibile determinare l'agente per '{action}'.",
            details={"action": action},
        )


class PermissionDeniedError(ApiError):
    code = "api.permission.denied"

    def __init__(self, action: str):
        super().__init__(
            f"Permesso negato per '{action}'.",
            details={"action": action},
        )
