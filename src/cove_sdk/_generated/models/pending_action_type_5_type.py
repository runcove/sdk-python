from enum import StrEnum


class PendingActionType5Type(StrEnum):
    WAKE = "wake"

    def __str__(self) -> str:
        return str(self.value)
