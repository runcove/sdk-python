from enum import StrEnum


class DenyReasonType14Code(StrEnum):
    TEAM_RAM_QUOTA_EXCEEDED = "team_ram_quota_exceeded"

    def __str__(self) -> str:
        return str(self.value)
