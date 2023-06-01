from enum import Enum, auto


class SymbolType(int, Enum):
    STRUCT_SYMBOL = auto()
    STRUCT_FIELD_SYMBOL = auto()
