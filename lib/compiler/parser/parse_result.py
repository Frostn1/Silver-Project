import dataclasses
from typing import Optional

from lib.compiler.parse_tree.parse_tree import ParseTree
from lib.compiler.symbol_table.symbol.symbol import Symbol


@dataclasses.dataclass
class ParseResult:
    tree: ParseTree
    symbol: Optional[Symbol] = None
