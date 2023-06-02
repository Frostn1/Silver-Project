from typing import List

from lib.compiler.error_handlers.handlers import raise_unexpected_term_error, raise_missing_term_error
from lib.compiler.lexer.enum_token_type import EnumTokenType
from lib.compiler.lexer.token import Token
from lib.compiler.parser.block_parser import parse_block, parse_anonymous_block
from lib.compiler.parser.parser import Parser
from lib.compiler.parser.struct_parser import parse_struct
from lib.compiler.parser.utils import try_get_next_token


def struct_top_level(parser: Parser) -> None:
    # struct
    if parser.token.next and parser.token.next.type == EnumTokenType.IDENTIFIER:
        parse_result = parse_struct(parser)
        parser.tree.add_child(parse_result.tree)
        parser.table.add_symbol(parse_result.symbol.symbol_name, parse_result.symbol)
    else:
        raise_unexpected_term_error(parser.token, [EnumTokenType.STRUCT])


def block_top_level(parser: Parser) -> None:
    # block
    if not parser.token.next:
        raise_missing_term_error(parser.token, [EnumTokenType.LEFT_BRACE])
    elif parser.token.next.type == EnumTokenType.IDENTIFIER:
        # named struct
        parsed_result = parse_block(parser)
        parser.tree.add_child(parsed_result.tree)
        parser.table.add_symbol(parsed_result.symbol.symbol_name, parsed_result.symbol)
    elif parser.token.next.type == EnumTokenType.LEFT_BRACE:
        # anonymous struct
        parsed_result = parse_anonymous_block(parser)
        parser.tree.add_child(parsed_result.tree)
        parser.table.add_symbol(parsed_result.symbol.symbol_name, parsed_result.symbol)
    else:
        raise_unexpected_term_error(parser.token, [EnumTokenType.BLOCK])


TOP_LEVEL_PARSERS = {
    EnumTokenType.STRUCT: struct_top_level,
    EnumTokenType.BLOCK: block_top_level
}


def top_level(parser: Parser) -> None:
    if parser.token.type in TOP_LEVEL_PARSERS:
        TOP_LEVEL_PARSERS[parser.token.type](parser)
    else:
        raise_unexpected_term_error(parser.token, list(TOP_LEVEL_PARSERS.keys()))


def parse(tokens: List[Token]) -> Parser:
    parser = Parser(tokens[0])
    while parser.token.next:
        top_level(parser)
        parser.token = try_get_next_token(parser.token)

    return parser
