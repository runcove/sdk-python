from enum import StrEnum


class DenyReasonType8Code(StrEnum):
    PENDING_RESIZE_EXHAUSTED = "pending_resize_exhausted"

    def __str__(self) -> str:
        return str(self.value)
