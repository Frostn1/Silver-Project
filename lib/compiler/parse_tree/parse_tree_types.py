from enum import Enum, auto
from typing import Any


class ParseTreeType(str, Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
        return name

    MAIN = auto()
    STRUCT_DECLARATION = auto()
    STRUCT_FIELD = auto()
    STRUCT_FIELD_TYPE_ANNOTATION = auto()
    BLOCK_DECLARATION = auto()
    ANONYMOUS_BLOCK_DECLARATION = auto()
