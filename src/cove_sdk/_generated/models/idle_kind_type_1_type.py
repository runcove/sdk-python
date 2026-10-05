from enum import StrEnum


class IdleKindType1Type(StrEnum):
    IDLE = "idle"

    def __str__(self) -> str:
        return str(self.value)
