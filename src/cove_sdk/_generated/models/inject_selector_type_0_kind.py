from enum import StrEnum


class InjectSelectorType0Kind(StrEnum):
    ALL = "all"

    def __str__(self) -> str:
        return str(self.value)
