from enum import StrEnum


class DiskFormat(StrEnum):
    QCOW2 = "qcow2"
    RAW = "raw"

    def __str__(self) -> str:
        return str(self.value)
