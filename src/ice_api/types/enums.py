from enum import Enum


class ActionDomain(str, Enum):
    LOGS = "logs"
    CODE = "code"
    KNOWLEDGE = "knowledge"
    WORKFLOW = "workflow"
    SYSTEM = "system"
    WORKSPACE = "workspace"
    UI = "ui"
    LLM = "llm"
    OTHER = "other"


class ActionKind(str, Enum):
    QUERY = "query"           # read-only
    MUTATION = "mutation"     # modifica stato
    ANALYSIS = "analysis"     # analisi / insight
    PLAN = "plan"             # pianificazione
    GENERATION = "generation" # output generativo

class ResultStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    PENDING = "pending"


class LifecyclePhase(str, Enum):
    PREBOOT = "preboot"
    BOOTSTRAP = "bootstrap"
    RUNTIME = "runtime"
    SHUTDOWN = "shutdown"


class IPCMessageKind(str, Enum):
    REQUEST = "request"
    RESPONSE = "response"
    EVENT = "event"
    ERROR = "error"
