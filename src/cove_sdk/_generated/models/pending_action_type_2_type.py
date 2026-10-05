from enum import StrEnum


class PendingActionType2Type(StrEnum):
    DISK_RESIZE_UP = "disk_resize_up"

    def __str__(self) -> str:
        return str(self.value)
