from enum import StrEnum


class OffboardVmOutcome(StrEnum):
    ALREADY_STOPPED = "already_stopped"
    FAILED = "failed"
    STOPPED = "stopped"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
