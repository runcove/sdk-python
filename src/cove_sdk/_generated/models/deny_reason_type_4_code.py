from enum import StrEnum


class DenyReasonType4Code(StrEnum):
    VM_LIMIT_EXCEEDED = "vm_limit_exceeded"

    def __str__(self) -> str:
        return str(self.value)
