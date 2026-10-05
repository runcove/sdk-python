from enum import StrEnum


class DenyReasonType2Code(StrEnum):
    DISK_SOFT_LIMIT_EXCEEDED = "disk_soft_limit_exceeded"

    def __str__(self) -> str:
        return str(self.value)
