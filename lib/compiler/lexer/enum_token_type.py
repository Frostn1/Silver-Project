from enum import Enum


class EnumTokenType(int, Enum):
    LEFT_CHEVRON = 0
    RIGHT_CHEVRON = 1
    LEFT_BRACE = 2
    RIGHT_BRACE = 3
    IDENTIFIER = 4
    COLON = 5
