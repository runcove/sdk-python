from enum import StrEnum


class AdminBulkScopeType1Type(StrEnum):
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
