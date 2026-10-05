from enum import StrEnum


class DenyReasonType1Code(StrEnum):
    CPU_HEADROOM_EXCEEDED = "cpu_headroom_exceeded"

    def __str__(self) -> str:
        return str(self.value)
