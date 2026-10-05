from enum import StrEnum


class CheckpointState(StrEnum):
    AVAILABLE = "available"
    CREATING = "creating"
    FAILED = "failed"
    RESTORING = "restoring"

    def __str__(self) -> str:
        return str(self.value)
