import dataclasses
from typing import List

from lib.compiler.symbol_table.symbol.symbol import Symbol
from lib.compiler.types.types import LanguageType


@dataclasses.dataclass
class StructFieldSymbol(Symbol):
    type: LanguageType


@dataclasses.dataclass
class StructSymbol(Symbol):
    fields: List[StructFieldSymbol]

    def add_field(self, field: StructFieldSymbol):
        self.fields.append(field)
