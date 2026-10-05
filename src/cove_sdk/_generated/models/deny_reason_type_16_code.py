from enum import StrEnum


class DenyReasonType16Code(StrEnum):
    TEAM_DISK_QUOTA_EXCEEDED = "team_disk_quota_exceeded"

    def __str__(self) -> str:
        return str(self.value)
