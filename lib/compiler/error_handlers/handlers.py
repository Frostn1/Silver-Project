from lib.compiler.error_handlers.error_config import ERROR_POSITION_FORMAT
from lib.compiler.error_handlers.exceptions import MissingTerm, InvalidTerm
from lib.compiler.lexer.token import Token


def raise_missing_term_error(token: Token, expecting_msg: str = None) -> None:
    raw_position = ERROR_POSITION_FORMAT.format(row=token.position.row, start_column=token.position.column,
                                                end_column=token.position.column + len(token.raw))
    expect_msg = f' , expecting {expecting_msg}' if expecting_msg else ''
    raise MissingTerm(f'Missing term at {raw_position}{expect_msg}')


def raise_invalid_term_error(token: Token, expecting_msg: str = None) -> None:
    raw_position = ERROR_POSITION_FORMAT.format(row=token.position.row, start_column=token.position.column,
                                                end_column=token.position.column + len(token.raw))
    expect_msg = f' , expecting {expecting_msg}' if expecting_msg else ''
    raise InvalidTerm(f'Invalid term at {raw_position}{expect_msg}')
