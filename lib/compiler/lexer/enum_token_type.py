from enum import Enum, auto
from typing import Any


class EnumTokenType(str, Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
        return name

    LEFT_CHEVRON = auto()
    RIGHT_CHEVRON = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    IDENTIFIER = auto()
    COLON = auto()
    COMMA = auto()
    STRUCT = auto()
    BLOCK = auto()
