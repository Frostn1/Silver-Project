import uuid

from lib.compiler.error_handlers.handlers import raise_missing_term_error
from lib.compiler.lexer.enum_token_type import EnumTokenType
from lib.compiler.parse_tree.parse_tree import ParseTree
from lib.compiler.parse_tree.parse_tree_types import ParseTreeType
from lib.compiler.parser.parse_result import ParseResult
from lib.compiler.parser.parser import Parser
from lib.compiler.parser.utils import get_next_token
from lib.compiler.symbol_table.symbol.block_symbol import BlockSymbol
from lib.compiler.symbol_table.symbol_type import SymbolType


def _generate_random_name() -> str:
    return str(uuid.uuid4())


def _parse_start_of_block(parser: Parser, block_name: str = None) -> ParseResult:
    parser.token = get_next_token(parser.token, expecting_msg='block name')
    block_name = block_name if block_name else parser.token.raw
    block_symbol = BlockSymbol(SymbolType.BLOCK_SYMBOL, block_name, parser.token.position, [], [])
    block_tree = ParseTree(ParseTreeType.BLOCK_DECLARATION)
    parser.token = get_next_token(parser.token, expecting_msg='opening brace')
    if parser.token.type != EnumTokenType.LEFT_BRACE:
        raise_missing_term_error(parser.token, expecting_msg='opening brace')
    return ParseResult(block_tree, block_symbol)


def parse_block(parser: Parser) -> ParseResult:
    parse_result = _parse_start_of_block(parser)
    block_tree, block_symbol = parse_result.tree, parse_result.symbol

    # parse statements inside of block here

    parser.token = get_next_token(parser.token, expecting_msg='identifier or closing brace')
    if parser.token.type != EnumTokenType.RIGHT_BRACE:
        raise_missing_term_error(parser.token, expecting_msg='closing brace')
    return ParseResult(block_tree, block_symbol)


def parse_anonymous_block(parser: Parser) -> ParseResult:
    parse_result = _parse_start_of_block(parser, _generate_random_name())
    block_tree, block_symbol = parse_result.tree, parse_result.symbol

    # parse statements inside of block here

    if parser.token.type != EnumTokenType.RIGHT_BRACE:
        raise_missing_term_error(parser.token, expecting_msg='closing brace')
    return ParseResult(block_tree, block_symbol)
