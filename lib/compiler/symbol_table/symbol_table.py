from typing import Dict

from lib.compiler.symbol_table.symbol.symbol import Symbol


class SymbolTable:
    def __init__(self):
        # symbol name to symbol object
        self.symbols: Dict[str, Symbol] = {}

    def add_symbol(self, name: str, symbol: Symbol):
        self.symbols[name] = symbol

    def __getitem__(self, key):
        return self.symbols.get(key)

    def __repr__(self) -> str:
        representation = ''
        representation += '================\n'
        representation += '= SYMBOL TABLE =\n'
        representation += '================\n'
        for _, symbol_value in self.symbols.items():
            representation += symbol_value
        return representation
