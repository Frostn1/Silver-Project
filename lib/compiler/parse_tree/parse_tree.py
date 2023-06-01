from typing import List

from lib.compiler.parse_tree.parse_tree_types import ParseTreeType


class ParseTree:
    def __init__(self, tree_type: ParseTreeType, children: List = None, value: str = '') -> None:
        self.tree_type: ParseTreeType = tree_type
        self.children: List[ParseTree] = children if children else []
        self.value: str = value

    def at(self, index: int) -> 'ParseTree':
        return self.children[index]

    def add_child(self, tree: 'ParseTree') -> None:
        self.children.append(tree)
