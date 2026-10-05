from enum import StrEnum


class DenyReasonType3Code(StrEnum):
    DISK_SAFETY_BUFFER_EXCEEDED = "disk_safety_buffer_exceeded"

    def __str__(self) -> str:
        return str(self.value)
