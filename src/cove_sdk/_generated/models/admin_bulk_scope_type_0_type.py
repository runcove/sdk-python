from enum import StrEnum


class AdminBulkScopeType0Type(StrEnum):
    ALL = "all"

    def __str__(self) -> str:
        return str(self.value)
