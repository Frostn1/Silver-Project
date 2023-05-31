import dataclasses

from lib.compiler.lexer.position import Position
from lib.compiler.lexer.token_type import TokenType


@dataclasses.dataclass
class Token:
    position: Position
    type: TokenType
