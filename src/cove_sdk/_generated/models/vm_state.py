from enum import StrEnum


class VmState(StrEnum):
    CHECKPOINTING = "checkpointing"
    CREATING = "creating"
    DELETED = "deleted"
    DELETING = "deleting"
    FAILED = "failed"
    FORCE_STOPPING = "force_stopping"
    HIBERNATED = "hibernated"
    HIBERNATING = "hibernating"
    PAUSED = "paused"
    PAUSING = "pausing"
    POOLED = "pooled"
    RESUMING = "resuming"
    RUNNING = "running"
    STOPPED = "stopped"
    STOPPING = "stopping"
    WAKING = "waking"

    def __str__(self) -> str:
        return str(self.value)
