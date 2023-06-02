import dataclasses
from typing import Any, List

from lib.compiler.lexer.enum_token_type import EnumTokenType


@dataclasses.dataclass
class TokenType:
    raw: str
    representation: str
    short_representation: EnumTokenType

    include_original: bool = False

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, EnumTokenType):
            return self.short_representation == other
        elif isinstance(other, str):
            return self.raw == other
        elif isinstance(other, TokenType):
            return self.short_representation == other.short_representation
        return False

    def __hash__(self) -> int:
        return hash(self.short_representation)

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __copy__(self):
        return TokenType(self.raw, self.representation, self.short_representation)


IDENTIFIER_TOKEN_TYPE = TokenType('', 'Custom Identifier', EnumTokenType.IDENTIFIER, True)

token_types: List[TokenType] = [
    TokenType('<', 'Left Chevron', EnumTokenType.LEFT_CHEVRON),
    TokenType('>', 'Left Chevron', EnumTokenType.RIGHT_CHEVRON),
    TokenType('{', 'Left Brace ', EnumTokenType.LEFT_BRACE),
    TokenType('}', 'Right Brace', EnumTokenType.RIGHT_BRACE),

    IDENTIFIER_TOKEN_TYPE,

    TokenType(':', 'Colon', EnumTokenType.COLON),
    TokenType(',', 'Comma', EnumTokenType.COMMA),
    TokenType('struct', 'Struct', EnumTokenType.STRUCT),
    TokenType('block', 'Block', EnumTokenType.BLOCK),
]
