from enum import StrEnum


class PendingActionType1Type(StrEnum):
    RESIZE_UP = "resize_up"

    def __str__(self) -> str:
        return str(self.value)
