from typing import List

from lib.compiler.error_handlers.error_config import ERROR_POSITION_FORMAT
from lib.compiler.error_handlers.exceptions import MissingTerm, InvalidTerm, UnexpectedTerm
from lib.compiler.lexer.enum_token_type import EnumTokenType
from lib.compiler.lexer.token import Token

POINTER_CHARACTER = '^'
SPACER_CHARACTER = '-'


def _get_info(token: Token) -> str:
    if token.raw:
        return token.raw
    elif token.type.raw:
        return token.type.raw
    return ''


def _try_parse_error_message(token: Token) -> str:
    messages = []
    if token.prev:
        messages.append(_get_info(token.prev))
    messages.append(_get_info(token))
    if token.next:
        messages.append(_get_info(token.next))
    return ' '.join(messages)


def _get_position_format(token: Token) -> str:
    return ERROR_POSITION_FORMAT.format(row=token.position.row, start_column=token.position.column,
                                        end_column=token.position.column + len(token.raw))


def _format_error(expect_token_types: List[EnumTokenType]) -> str:
    return ' expecting ' + f"( {' , '.join(expect_token_types)} )"


def _get_error_info_message(token: Token) -> str:
    suffix = SPACER_CHARACTER * token.position.column
    suffix = ''
    token_raw = ''
    if token.raw:
        token_raw = token.raw
    elif token.type.raw:
        token_raw = token.type.raw
    postfix = POINTER_CHARACTER * len(token_raw)
    return suffix + postfix


def _get_full_message(token: Token, expect_token_types: List[EnumTokenType]) -> str:
    error_pre_suffix = '\t'
    raw_position = _get_position_format(token)
    expect_msg = _format_error(expect_token_types)
    info_message = error_pre_suffix + _try_parse_error_message(token)
    error_message = error_pre_suffix + _get_error_info_message(token)
    return f'{raw_position}{expect_msg}\n{info_message}\n{error_message}'


def raise_missing_term_error(token: Token, expect_token_types: List[EnumTokenType]) -> None:
    full_message = _get_full_message(token, expect_token_types)
    raise MissingTerm(f'Missing term at {full_message}')


def raise_invalid_term_error(token: Token, expect_token_types: List[EnumTokenType]) -> None:
    full_message = _get_full_message(token, expect_token_types)
    raise InvalidTerm(f'Invalid term at {full_message}')


def raise_unexpected_term_error(token: Token, expect_token_types: List[EnumTokenType]) -> None:
    full_message = _get_full_message(token, expect_token_types)
    raise UnexpectedTerm(f'Unexpected term at {full_message}')
