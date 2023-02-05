from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from account.domain import events


@dataclass(eq=False)
class Account:
    account_number: str
    user_id: str
    name: str
    cash: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    events: List[events.Event] = field(default_factory=list)

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return self.account_number == other.account_number
        return False

    def __hash__(self) -> int:
        return hash(self.account_number)

    # 출금
    def withdraw(self, amount: int):
        if self.cash < amount:
            self.events.append(
                events.InsufficientCash(account_number=self.account_number)
            )
        else:
            self.cash -= amount
            self.events.append(
                events.Withdrew(account_number=self.account_number, amount=amount)
            )

    # 입금
    def deposit(self, amount: int):
        self.cash += amount
        self.events.append(
            events.Deposited(account_number=self.account_number, amount=amount)
        )
