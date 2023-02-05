from dataclasses import dataclass


class Command:
    pass


@dataclass
class Opened(Command):
    user_id: str
    name: str
    cash: int = 0


@dataclass
class Withdraw(Command):
    account_number: str
    amount: int


@dataclass
class Deposit(Command):
    account_number: str
    amount: int
