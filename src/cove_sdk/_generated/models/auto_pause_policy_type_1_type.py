from enum import StrEnum


class AutoPausePolicyType1Type(StrEnum):
    ALWAYS_ON = "always_on"

    def __str__(self) -> str:
        return str(self.value)
