from typing import Tuple

from lib.compiler.error_handlers.handlers import raise_invalid_term_error, raise_missing_term_error
from lib.compiler.lexer.enum_token_type import EnumTokenType
from lib.compiler.parse_tree.parse_tree import ParseTree
from lib.compiler.parse_tree.parse_tree_types import ParseTreeType
from lib.compiler.parser.parse_result import ParseResult
from lib.compiler.parser.parser import Parser
from lib.compiler.parser.utils import get_next_token
from lib.compiler.symbol_table.symbol.sturct_symbol import StructSymbol, StructFieldSymbol
from lib.compiler.symbol_table.symbol_type import SymbolType
from lib.compiler.types.types import LanguageType


def parse_type(parser: Parser) -> Tuple[ParseTree, LanguageType]:
    # field has type
    # for now just check that type is an identifier

    if parser.token.next.type != EnumTokenType.IDENTIFIER:
        raise_invalid_term_error(parser.token, expecting_msg='type name')
    parser.token = get_next_token(parser.token, expecting_msg='type name')
    field_type_tree = ParseTree(ParseTreeType.STRUCT_FIELD_TYPE_ANNOTATION, value=parser.token.raw)
    parser.token = get_next_token(parser.token, expecting_msg='next field or end of struct')
    return field_type_tree, LanguageType.UNDEFINED


def parse_struct_field(parser: Parser) -> ParseResult:
    if parser.token.type != EnumTokenType.IDENTIFIER:
        raise_invalid_term_error(parser.token, expecting_msg='identifier')
    field_name = parser.token.raw  # for symbol table later
    field_symbol = StructFieldSymbol(SymbolType.STRUCT_FIELD_SYMBOL, field_name, parser.token.position, [],
                                     LanguageType.ANY)
    field_tree = ParseTree(ParseTreeType.STRUCT_FIELD)
    parser.token = get_next_token(parser.token, expecting_msg='comma or colon')

    if parser.token.type == EnumTokenType.COLON:
        field_type_tree, field_symbol.type = parse_type(parser)
        field_tree.add_child(field_type_tree)

    if parser.token.type == EnumTokenType.COMMA:
        parser.token = get_next_token(parser.token, expecting_msg='closing brace')

    return ParseResult(field_tree, field_symbol)


def parse_struct(parser: Parser) -> ParseResult:
    parser.token = get_next_token(parser.token, expecting_msg='struct name')
    struct_name = parser.token.raw
    struct_symbol = StructSymbol(SymbolType.STRUCT_SYMBOL, struct_name, parser.token.position, [], [])
    struct_tree = ParseTree(ParseTreeType.STRUCT_DECLARATION)
    parser.token = get_next_token(parser.token, expecting_msg='opening brace')
    parser.token = get_next_token(parser.token, expecting_msg='identifier or closing brace')
    while parser.token.type == EnumTokenType.IDENTIFIER:
        parse_result = parse_struct_field(parser)
        struct_symbol.add_field(parse_result.symbol)
        struct_tree.add_child(parse_result.tree)
    if parser.token.type != EnumTokenType.RIGHT_BRACE:
        raise_missing_term_error(parser.token, expecting_msg='closing brace')
    return ParseResult(struct_tree, struct_symbol)
