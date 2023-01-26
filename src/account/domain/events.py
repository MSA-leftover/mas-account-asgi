from dataclasses import dataclass
from typing import Optional


class Event:
    pass


@dataclass
class IsExistedAccount(Event):
    account_number: str


@dataclass
class InsufficientCash(Event):
    account_number: str



@dataclass
class AccountOpened(Event):
    account_number: str
    name: str
    amount: Optional[int]


@dataclass
class AccountClosed(Event):
    account_number: str


@dataclass
class Withdrew(Event):
    account_number: str
    amount: int


@dataclass
class Deposited(Event):
    account_number: str
    amount: int
