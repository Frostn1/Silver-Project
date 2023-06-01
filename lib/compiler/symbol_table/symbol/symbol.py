import dataclasses
from typing import List

from lib.compiler.lexer.position import Position
from lib.compiler.symbol_table.symbol_type import SymbolType


@dataclasses.dataclass
class Symbol:
    symbol_type: SymbolType
    symbol_name: str
    declaration_position: Position
    usage_positions: List[Position]

    def __repr__(self) -> str:
        representation = ''
        representation += f'[ {self.symbol_name} ] ( {self.symbol_type} )\n'
        representation += f'> DECLARATION {self.declaration_position}\n'
        return representation

    def __str__(self) -> str:
        return self.__repr__()
