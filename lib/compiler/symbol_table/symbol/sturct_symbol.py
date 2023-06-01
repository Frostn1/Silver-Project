import dataclasses
from typing import List

from lib.compiler.symbol_table.symbol.symbol import Symbol
from lib.compiler.types.types import LanguageType


@dataclasses.dataclass
class StructFieldSymbol(Symbol):
    type: LanguageType

    def __repr__(self) -> str:
        representation = ''
        representation += f'< FIELD > [ {self.symbol_name} ] ( {self.type} )\n'
        return representation


@dataclasses.dataclass
class StructSymbol(Symbol):
    fields: List[StructFieldSymbol]

    def add_field(self, field: StructFieldSymbol):
        self.fields.append(field)

    def __repr__(self) -> str:
        representation = super().__repr__()
        for field in self.fields:
            representation += field
        return representation
