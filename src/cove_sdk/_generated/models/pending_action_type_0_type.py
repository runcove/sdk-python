from enum import StrEnum


class PendingActionType0Type(StrEnum):
    CREATE = "create"

    def __str__(self) -> str:
        return str(self.value)
