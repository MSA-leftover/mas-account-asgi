from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime


class HistoryType(str, Enum):
    DEPOSIT = auto()
    WITHDRAW = auto()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


@dataclass
class History:
    account_number: str
    description: str
    amount: int
    type: HistoryType
    created_at: datetime = field(default_factory=datetime.now)
    other_account_number: str | None = None
