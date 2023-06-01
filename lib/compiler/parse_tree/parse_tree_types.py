from enum import Enum, auto


class ParseTreeType(int, Enum):
    MAIN = auto()
    STRUCT_DECLARATION = auto()
    STRUCT_FIELD = auto()
    STRUCT_FIELD_TYPE_ANNOTATION = auto()
