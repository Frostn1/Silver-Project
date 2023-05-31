from typing import List, Any
from string import whitespace, punctuation

from lib.compiler.lexer.position import Position
from lib.compiler.lexer.token import Token
from lib.compiler.lexer.token_type import token_types, TokenType

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


def get_next_token_type(current_slice: str) -> TokenType:
    if current_slice in token_types:
        return token_types[token_types.index(current_slice)]
    else:
        print(f'[ Token doesnt exist in file : {current_slice} ]')


def idk(file_content: str) -> Any:
    length = len(file_content)
    current_index = 0
    current_slice = ''
    current_position = Position(1, 1)
    while current_index < length:
        current_char = file_content[current_index]
        if _is_space(current_char) and current_slice:
            get_next_token_type(current_slice)
            current_slice = ''
        elif current_char in punctuation:
            current_slice += current_char
            get_next_token_type(current_slice)
            current_slice = ''
        elif not _is_space(current_char):
            current_slice += current_char

        if current_char == NEW_LINE_CHARACTER:
            current_position.row += 1
            current_position.column = 1
        else:
            current_position.column += 1
        current_index += 1


def lex(file_content: str) -> List[Token]:
    idk(file_content)
    return []
