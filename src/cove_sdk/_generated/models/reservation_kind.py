from enum import StrEnum


class ReservationKind(StrEnum):
    CLONE = "clone"
    CREATE = "create"
    DISK_RESIZE_UP = "disk_resize_up"
    POOL_REFILL = "pool_refill"
    RESIZE_UP = "resize_up"
    WAKE = "wake"
    WAKE_FROM_CHECKPOINT = "wake_from_checkpoint"

    def __str__(self) -> str:
        return str(self.value)
