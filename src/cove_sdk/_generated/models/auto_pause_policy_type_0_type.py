from enum import StrEnum


class AutoPausePolicyType0Type(StrEnum):
    AUTO_PAUSE = "auto_pause"

    def __str__(self) -> str:
        return str(self.value)
