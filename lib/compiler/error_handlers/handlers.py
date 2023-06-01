from lib.compiler.error_handlers.error_config import ERROR_POSITION_FORMAT
from lib.compiler.error_handlers.exceptions import MissingTerm, InvalidTerm, UnexpectedTerm
from lib.compiler.lexer.token import Token


def _get_position_format(token: Token) -> str:
    return ERROR_POSITION_FORMAT.format(row=token.position.row, start_column=token.position.column,
                                        end_column=token.position.column + len(token.raw))


def raise_missing_term_error(token: Token, expecting_msg: str = None) -> None:
    raw_position = _get_position_format(token)
    expect_msg = f' , missing {expecting_msg}' if expecting_msg else ''
    raise MissingTerm(f'Missing term at {raw_position}{expect_msg}')


def raise_invalid_term_error(token: Token, expecting_msg: str = None) -> None:
    raw_position = _get_position_format(token)
    expect_msg = f' , expecting {expecting_msg}' if expecting_msg else ''
    raise InvalidTerm(f'Invalid term at {raw_position}{expect_msg}')


def raise_unexpected_term_error(token: Token, expecting_msg: str = None) -> None:
    raw_position = _get_position_format(token)
    expect_msg = f' , can\'t parse {expecting_msg}' if expecting_msg else ''
    raise UnexpectedTerm(f'Unexpected term at {raw_position}{expect_msg}')
