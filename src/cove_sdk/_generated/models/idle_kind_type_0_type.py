from enum import StrEnum


class IdleKindType0Type(StrEnum):
    ACTIVE = "active"

    def __str__(self) -> str:
        return str(self.value)
