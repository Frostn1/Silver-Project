from typing import List

from lib.compiler.lexer.enum_token_type import EnumTokenType
from lib.compiler.lexer.token import Token
from lib.compiler.parser.parser import Parser
from lib.compiler.parser.struct_parser import parse_struct
from lib.compiler.parser.utils import get_next_token


def identifier_top_level(parser: Parser) -> None:
    # struct block
    parser.token = get_next_token(parser.token)
    if parser.token.type == EnumTokenType.LEFT_BRACE:
        parse_struct(parser)


def top_level(parser: Parser) -> None:
    if parser.token.type == EnumTokenType.IDENTIFIER:
        identifier_top_level(parser)


def parse(tokens: List[Token]):
    parser = Parser(tokens[0])
    while parser.token.next:
        top_level(parser)
