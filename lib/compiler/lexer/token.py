import dataclasses
from typing import Optional

from lib.compiler.lexer.position import Position
from lib.compiler.lexer.token_type import token_types, TokenType, IDENTIFIER_TOKEN_TYPE

EMPTY_SLICE = ''


@dataclasses.dataclass
class Token:
    position: Position
    type: TokenType
    raw: str

    next: Optional['Token']
    prev: Optional['Token']


def _get_token_type(current_slice: str) -> TokenType:
    if current_slice in token_types:
        return token_types[token_types.index(current_slice)]
    else:
        return token_types[token_types.index(IDENTIFIER_TOKEN_TYPE)]


def get_token(current_slice: str, current_position: Position) -> Token:
    token_type = _get_token_type(current_slice)
    original_representation = current_slice if token_type.include_original else EMPTY_SLICE
    return Token(position=current_position, type=token_type, raw=original_representation, next=None, prev=None)
