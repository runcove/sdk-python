from enum import StrEnum


class DenyReasonType9Code(StrEnum):
    USER_VCPU_QUOTA_EXCEEDED = "user_vcpu_quota_exceeded"

    def __str__(self) -> str:
        return str(self.value)
