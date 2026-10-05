from enum import StrEnum


class ConnectedAppAccess(StrEnum):
    FULL = "full"
    NON_DESTRUCTIVE = "non_destructive"

    def __str__(self) -> str:
        return str(self.value)
