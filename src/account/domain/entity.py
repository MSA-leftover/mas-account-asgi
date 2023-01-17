from dataclasses import dataclass


@dataclass(eq=False)
class Account:
    id: str
    user_id: str
    name: str
    amount: int

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self.id == other.id
        return False

    def __hash__(self) -> int:
        return hash(self.id)
