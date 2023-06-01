from enum import auto, Enum


class LanguageType(int, Enum):
    TEXT = auto()
    NUMBER = auto()
    BOOL = auto()
