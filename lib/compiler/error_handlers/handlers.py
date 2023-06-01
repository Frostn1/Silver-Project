from typing import List

from lib.compiler.error_handlers.error_config import ERROR_POSITION_FORMAT
from lib.compiler.error_handlers.exceptions import MissingTerm, InvalidTerm, UnexpectedTerm
from lib.compiler.lexer.enum_token_type import EnumTokenType
from lib.compiler.lexer.token import Token


def _get_position_format(token: Token) -> str:
    return ERROR_POSITION_FORMAT.format(row=token.position.row, start_column=token.position.column,
                                        end_column=token.position.column + len(token.raw))


def _format_error(expect_token_types: List[EnumTokenType]) -> str:
    return 'expecting ' + ' or '.join(expect_token_types)


def raise_missing_term_error(token: Token, expect_token_types: List[EnumTokenType]) -> None:
    raw_position = _get_position_format(token)
    expect_msg = _format_error(expect_token_types)
    raise MissingTerm(f'Missing term at {raw_position}{expect_msg}')


def raise_invalid_term_error(token: Token, expect_token_types: List[EnumTokenType]) -> None:
    raw_position = _get_position_format(token)
    expect_msg = _format_error(expect_token_types)
    raise InvalidTerm(f'Invalid term at {raw_position}{expect_msg}')


def raise_unexpected_term_error(token: Token, expect_token_types: List[EnumTokenType]) -> None:
    raw_position = _get_position_format(token)
    expect_msg = _format_error(expect_token_types)
    raise UnexpectedTerm(f'Unexpected term at {raw_position}{expect_msg}')
