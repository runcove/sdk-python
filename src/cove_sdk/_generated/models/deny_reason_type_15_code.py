from enum import StrEnum


class DenyReasonType15Code(StrEnum):
    TEAM_VM_COUNT_QUOTA_EXCEEDED = "team_vm_count_quota_exceeded"

    def __str__(self) -> str:
        return str(self.value)
