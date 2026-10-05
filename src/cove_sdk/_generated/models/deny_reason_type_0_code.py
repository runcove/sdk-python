from enum import StrEnum


class DenyReasonType0Code(StrEnum):
    RAM_HEADROOM_EXCEEDED = "ram_headroom_exceeded"

    def __str__(self) -> str:
        return str(self.value)
