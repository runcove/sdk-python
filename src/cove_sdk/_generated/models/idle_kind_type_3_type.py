from enum import StrEnum


class IdleKindType3Type(StrEnum):
    NOT_RUNNING = "not_running"

    def __str__(self) -> str:
        return str(self.value)
