from enum import StrEnum


class AdminBulkScopeType2Type(StrEnum):
    VMS = "vms"

    def __str__(self) -> str:
        return str(self.value)
