from enum import StrEnum


class TrafficMonitorBackend(StrEnum):
    EBPF = "ebpf"
    NONE = "none"
    RELAY = "relay"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
