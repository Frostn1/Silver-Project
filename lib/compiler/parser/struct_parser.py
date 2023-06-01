from lib.compiler.error_handlers.handlers import raise_invalid_term_error, raise_missing_term_error
from lib.compiler.lexer.enum_token_type import EnumTokenType
from lib.compiler.parser.parser import Parser
from lib.compiler.parser.utils import get_next_token


def parse_struct_field(parser: Parser) -> None:
    if parser.token.type != EnumTokenType.IDENTIFIER:
        raise_invalid_term_error(parser.token, expecting_msg='identifier')
    field_name = parser.token.raw  # for symbol table later
    parser.token = get_next_token(parser.token, expecting_msg='comma or colon')
    if parser.token.type == EnumTokenType.COLON:
        # field has type
        # for now just check that type is an identifier
        if parser.token.next.type != EnumTokenType.IDENTIFIER:
            raise_invalid_term_error(parser.token, expecting_msg='identifier')
        parser.token = get_next_token(parser.token, expecting_msg='next field or end of struct')
    if parser.token.type == EnumTokenType.COMMA:
        parser.token = get_next_token(parser.token, expecting_msg='closing brace')


def parse_struct(parser: Parser) -> None:
    struct_name = parser.token.raw
    parser.token = get_next_token(parser.token, expecting_msg='closing brace')
    while parser.token.type == EnumTokenType.IDENTIFIER:
        parse_struct_field(parser)
        # parse current line in struct
    if parser.token.type != EnumTokenType.RIGHT_BRACE:
        raise_missing_term_error(parser.token, expecting_msg='closing brace')
