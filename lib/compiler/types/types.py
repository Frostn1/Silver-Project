from enum import auto, Enum


class LanguageType(int, Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
        return name

    TEXT = auto()
    NUMBER = auto()
    BOOL = auto()
    ANY = auto()

    UNDEFINED = auto()
