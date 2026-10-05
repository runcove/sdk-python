from enum import StrEnum


class DenyReasonType13Code(StrEnum):
    TEAM_VCPU_QUOTA_EXCEEDED = "team_vcpu_quota_exceeded"

    def __str__(self) -> str:
        return str(self.value)
