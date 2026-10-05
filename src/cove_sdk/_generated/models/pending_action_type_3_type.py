from enum import StrEnum


class PendingActionType3Type(StrEnum):
    WAKE_FROM_CHECKPOINT = "wake_from_checkpoint"

    def __str__(self) -> str:
        return str(self.value)
