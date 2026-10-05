from enum import StrEnum


class DenyReasonType10Code(StrEnum):
    USER_RAM_QUOTA_EXCEEDED = "user_ram_quota_exceeded"

    def __str__(self) -> str:
        return str(self.value)
