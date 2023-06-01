import dataclasses


@dataclasses.dataclass
class Position:
    row: int
    column: int

    def __repr__(self) -> str:
        return f'{self.row}::{self.column}'
