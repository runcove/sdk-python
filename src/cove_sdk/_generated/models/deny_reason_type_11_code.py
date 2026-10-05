from enum import StrEnum


class DenyReasonType11Code(StrEnum):
    USER_VM_COUNT_QUOTA_EXCEEDED = "user_vm_count_quota_exceeded"

    def __str__(self) -> str:
        return str(self.value)
