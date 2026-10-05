from enum import StrEnum


class DenyReasonType6Code(StrEnum):
    PRESSURE_DENIED_PSI = "pressure_denied_psi"

    def __str__(self) -> str:
        return str(self.value)
