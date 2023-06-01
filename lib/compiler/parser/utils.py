from typing import Optional, List

from lib.compiler.error_handlers.handlers import raise_missing_term_error, raise_unexpected_term_error
from lib.compiler.lexer.enum_token_type import EnumTokenType
from lib.compiler.lexer.token import Token


def get_next_token(token: Token, expect_token_types: Optional[List[EnumTokenType]] = None):
    if token.next is None:
        raise_missing_term_error(token, expect_token_types)
    if expecting_token_type and token.type.short_representation not in expect_token_types:
        raise_unexpected_term_error(token, expect_token_types)
    return token.next


def try_get_next_token(token):
    if token.next is None:
        return token
    return token.next
