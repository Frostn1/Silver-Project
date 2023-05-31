from lib.compiler.lexer.enum_token_type import EnumTokenType
from lib.compiler.lexer.token import Token


def parse_struct_field(token: Token) -> None:
    if token.type != EnumTokenType.IDENTIFIER:
        # raise error of missing identifier name
    identifier_name = token.raw
    token = token.next
    if token.type == EnumTokenType.COLON:
        # field has type


def parse_struct(token: Token) -> None:
    token = token.next
    while token.type == EnumTokenType.IDENTIFIER:
        pass
        # parse current line in struct
    if token.type != EnumTokenType.RIGHT_BRACE:
        # raise error of missing brace
        pass
