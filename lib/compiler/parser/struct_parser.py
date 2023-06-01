from typing import Optional

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


def parse_struct_field(parser: Parser) -> ParseResult:
    if parser.token.type != EnumTokenType.IDENTIFIER:
        raise_invalid_term_error(parser.token, expecting_msg='identifier')
    field_name = parser.token.raw  # for symbol table later
    field_symbol = StructFieldSymbol(SymbolType.STRUCT_FIELD_SYMBOL, field_name, parser.token.position, [],
                                     LanguageType.ANY)
    field_tree = ParseTree(ParseTreeType.STRUCT_FIELD)
    field_type_tree: Optional[ParseTree] = None
    parser.token = get_next_token(parser.token, expecting_msg='comma or colon')
    if parser.token.type == EnumTokenType.COLON:
        # field has type
        # for now just check that type is an identifier
        if parser.token.next.type != EnumTokenType.IDENTIFIER:
            raise_invalid_term_error(parser.token, expecting_msg='identifier')
        field_symbol.type = LanguageType.UNDEFINED
        field_type_tree = ParseTree(ParseTreeType.STRUCT_FIELD_TYPE_ANNOTATION, value=parser.token.raw)
        parser.token = get_next_token(parser.token, expecting_msg='next field or end of struct')
    if parser.token.type == EnumTokenType.COMMA:
        parser.token = get_next_token(parser.token, expecting_msg='closing brace')
    if field_type_tree:
        field_tree.add_child(field_type_tree)

    return ParseResult(field_tree, field_symbol)


def parse_struct(parser: Parser) -> ParseResult:
    struct_name = parser.token.raw
    struct_symbol = StructSymbol(SymbolType.STRUCT_SYMBOL, struct_name, parser.token.position, [], [])
    struct_tree = ParseTree(ParseTreeType.STRUCT_DECLARATION)
    parser.token = get_next_token(parser.token, expecting_msg='closing brace')
    while parser.token.next and parser.token.next.type == EnumTokenType.IDENTIFIER:
        parser.token = get_next_token(parser.token, expecting_msg='identifier')
        parse_result = parse_struct_field(parser)
        struct_symbol.add_field(parse_result.symbol)
        struct_tree.add_child(parse_result.tree)
    if parser.token.type != EnumTokenType.RIGHT_BRACE:
        raise_missing_term_error(parser.token, expecting_msg='closing brace')

    return ParseResult(struct_tree, struct_symbol)
