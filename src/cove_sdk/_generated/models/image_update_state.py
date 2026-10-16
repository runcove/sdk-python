from enum import StrEnum


class ImageUpdateState(StrEnum):
    AVAILABLE = "available"
    FAILED = "failed"
    UNKNOWN = "unknown"
    UPDATING = "updating"
    UP_TO_DATE = "up_to_date"

    def __str__(self) -> str:
        return str(self.value)
