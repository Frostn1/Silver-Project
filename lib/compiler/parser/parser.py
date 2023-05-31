from typing import List

from lib.compiler.lexer.enum_token_type import EnumTokenType
from lib.compiler.lexer.token import Token
from lib.compiler.parser.result import Result
from lib.compiler.parser.struct_parser import parse_struct


def identifier_top_level(token: Token) -> Result:
    # struct block
    if token.next is None:
        # raise error
        return Result()
    if token.next.type == EnumTokenType.LEFT_BRACE:
        parse_struct(token)
def top_level(token: Token) -> Result:
    if token.type == EnumTokenType.IDENTIFIER:
        identifier_top_level(token)

def parse(tokens: List[Token]):
    ...
