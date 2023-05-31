from lib.compiler.error_handlers.handlers import raise_missing_term_error
from lib.compiler.lexer.token import Token


def get_next_token(token: Token, expecting_msg: str = None):
    if token.next is None:
        raise_missing_term_error(token, expecting_msg)
    return token.next
