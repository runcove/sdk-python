from enum import StrEnum


class DeleteAfterStopType0Type(StrEnum):
    NEVER = "never"

    def __str__(self) -> str:
        return str(self.value)
