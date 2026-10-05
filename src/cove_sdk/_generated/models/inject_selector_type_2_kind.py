from enum import StrEnum


class InjectSelectorType2Kind(StrEnum):
    SETUP_TAG = "setup_tag"

    def __str__(self) -> str:
        return str(self.value)
