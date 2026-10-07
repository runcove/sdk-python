from enum import StrEnum


class OffboardWarpgateRoleOutcome(StrEnum):
    DELETED = "deleted"
    FAILED = "failed"
    NOT_FOUND = "not_found"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
