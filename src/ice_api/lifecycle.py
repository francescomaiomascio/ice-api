from enum import Enum


class LifecyclePhase(str, Enum):
    BOOTSTRAP = "bootstrap"
    PREBOOT = "preboot"
    RUNTIME = "runtime"
    SHUTDOWN = "shutdown"
