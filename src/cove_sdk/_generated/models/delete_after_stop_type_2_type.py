from enum import StrEnum


class DeleteAfterStopType2Type(StrEnum):
    AFTER_SECS = "after_secs"

    def __str__(self) -> str:
        return str(self.value)
