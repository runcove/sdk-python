from enum import StrEnum


class DeliveryState(StrEnum):
    DELIVERED = "delivered"
    FAILED = "failed"
    IN_FLIGHT = "in_flight"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
