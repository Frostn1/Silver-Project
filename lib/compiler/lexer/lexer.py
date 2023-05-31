from typing import List, Any, Tuple
from string import whitespace, punctuation

from lib.compiler.lexer.position import Position
from lib.compiler.lexer.token import Token, get_token

SPACE_CHARACTER = whitespace
NEW_LINE_CHARACTER = '\n'


# person {
#
# }
#
#
#


def _is_space(current_char: chr) -> bool:
    return current_char in SPACE_CHARACTER


def get_next_char(file_content: str) -> str:
    length = len(file_content)
    current_index = 0
    while current_index < length:
        yield file_content[current_index]
        current_index += 1


def is_current_char_ending(current_char: str, current_slice: str) -> Tuple[str, bool]:
    if _is_space(current_char) and current_slice:
        return current_slice, True
    elif current_char in punctuation:
        if not current_slice:
            current_slice += current_char
        return current_slice, True
    elif not _is_space(current_char):
        current_slice += current_char
    return current_slice, False


def parse_new_position(old_position: Position, current_char: str) -> None:
    if current_char == NEW_LINE_CHARACTER:
        old_position.row += 1
        old_position.column = 1
    else:
        old_position.column += 1


def lex(file_content: str) -> List[Token]:
    current_slice = ''
    tokens: List[Token] = []
    current_position = Position(1, 1)
    start_position = Position(1, 1)
    for char in get_next_char(file_content):
        current_slice, is_ending = is_current_char_ending(char, current_slice)
        if is_ending:
            next_token = get_token(current_slice, start_position)
            if tokens:
                tokens[-1].next = next_token
            tokens.append(next_token)

            current_slice = char if char in punctuation and current_slice != char else ''
            start_position = Position(current_position.row, current_position.column)
        parse_new_position(current_position, char)
    return tokens
