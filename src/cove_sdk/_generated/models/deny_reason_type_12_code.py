from enum import StrEnum


class DenyReasonType12Code(StrEnum):
    USER_DISK_QUOTA_EXCEEDED = "user_disk_quota_exceeded"

    def __str__(self) -> str:
        return str(self.value)
