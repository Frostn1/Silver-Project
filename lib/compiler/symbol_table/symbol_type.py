from enum import Enum, auto
from typing import Any


class SymbolType(str, Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
        return name

    STRUCT_SYMBOL = auto()
    STRUCT_FIELD_SYMBOL = auto()
