from enum import StrEnum


class PendingActionType6Type(StrEnum):
    POOL_REFILL = "pool_refill"

    def __str__(self) -> str:
        return str(self.value)
