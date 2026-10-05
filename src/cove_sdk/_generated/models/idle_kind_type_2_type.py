from enum import StrEnum


class IdleKindType2Type(StrEnum):
    ALWAYS_ON = "always_on"

    def __str__(self) -> str:
        return str(self.value)
