from enum import StrEnum


class ResizeRestart(StrEnum):
    NOT_NEEDED = "not_needed"
    RESTARTED = "restarted"
    STOPPED = "stopped"

    def __str__(self) -> str:
        return str(self.value)
