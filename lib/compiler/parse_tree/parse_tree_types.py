from enum import Enum, auto


class ParseTreeType(int, Enum):
    MAIN = auto()
    STRUCT_DECLARATION = auto()
    STRUCT_FIELD = auto()
    STRUCT_FIELd_TYPE_ANNOTATION = auto()
