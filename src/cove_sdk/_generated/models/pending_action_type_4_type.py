from enum import StrEnum


class PendingActionType4Type(StrEnum):
    CLONE = "clone"

    def __str__(self) -> str:
        return str(self.value)
