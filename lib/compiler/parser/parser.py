from lib.compiler.lexer.token import Token
from lib.compiler.parse_tree.parse_tree import ParseTree
from lib.compiler.parse_tree.parse_tree_types import ParseTreeType
from lib.compiler.symbol_table.symbol_table import SymbolTable


class Parser:
    def __init__(self, start_token: Token):
        self.table: SymbolTable = SymbolTable()
        self.token: Token = start_token
        self.tree: ParseTree = ParseTree(ParseTreeType.MAIN)
