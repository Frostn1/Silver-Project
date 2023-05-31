import dataclasses
from typing import Any, List


@dataclasses.dataclass
class TokenType:
    raw: str
    representation: str
    short_representation: str

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return self.raw == other
        elif isinstance(other, TokenType):
            return self.short_representation == other.short_representation
        return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __copy__(self):
        return TokenType(self.raw, self.representation, self.short_representation)


token_types: List[TokenType] = [
    TokenType('<', 'Left Chevron', 'LEFT_CHEVRON'),
    TokenType('>', 'Left Chevron', 'RIGHT_CHEVRON'),
    TokenType('{', 'Left Brace ', 'LEFT_BRACE'),
    TokenType('}', 'Right Brace', 'RIGHT_BRACE'),


]
