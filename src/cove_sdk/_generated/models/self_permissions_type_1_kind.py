from enum import StrEnum


class SelfPermissionsType1Kind(StrEnum):
    SESSION = "session"

    def __str__(self) -> str:
        return str(self.value)
