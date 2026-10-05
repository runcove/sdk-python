from enum import StrEnum


class DenyReasonType5Code(StrEnum):
    PRESSURE_DENIED_MEM = "pressure_denied_mem"

    def __str__(self) -> str:
        return str(self.value)
