from typing import List
import dataclasses

from lib.compiler.symbol_table.symbol.symbol import Symbol


@dataclasses.dataclass
class BlockSymbol(Symbol):
    terms: List[Symbol]

    def add_field(self, terms: Symbol):
        self.terms.append(terms)

    def __repr__(self) -> str:
        representation = super().__repr__()
        for field in self.terms:
            representation += str(field)
        return representation

    def __str__(self) -> str:
        return self.__repr__()
