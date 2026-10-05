from enum import StrEnum


class DeleteAfterStopType1Type(StrEnum):
    IMMEDIATE = "immediate"

    def __str__(self) -> str:
        return str(self.value)
