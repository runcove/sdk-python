from enum import StrEnum


class DenyReasonType7Code(StrEnum):
    SWAP_PRESSURE_DENIED = "swap_pressure_denied"

    def __str__(self) -> str:
        return str(self.value)
