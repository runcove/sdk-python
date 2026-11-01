from enum import StrEnum


class TrafficMonitorState(StrEnum):
    DISABLED = "disabled"
    LOADED = "loaded"
    NOT_COMPILED = "not_compiled"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"
    UNSUPPORTED = "unsupported"
    WAKE_STOPPED = "wake_stopped"

    def __str__(self) -> str:
        return str(self.value)
