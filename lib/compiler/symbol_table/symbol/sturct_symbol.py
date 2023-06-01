import dataclasses

from lib.compiler.symbol_table.symbol.symbol import Symbol


@dataclasses.dataclass
class StructFieldSymbol(Symbol):
    name: str
    type: LanguageType


@dataclasses.dataclass
class StructSymbol(Symbol):
    fields: List[SturctFieldSymbol]
