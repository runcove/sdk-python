from enum import StrEnum


class InjectSelectorType1Kind(StrEnum):
    SUBSET = "subset"

    def __str__(self) -> str:
        return str(self.value)
