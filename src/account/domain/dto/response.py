from __future__ import annotations

from pydantic import BaseModel

from account.domain.entity import Account


class AccountResponseDTO(BaseModel):
    account_number: str
    name: str
    user_id: str
    cash: int

    @classmethod
    def build(cls, account: Account) -> AccountResponseDTO:
        return cls(
            account_number=account.account_number,
            name=account.name,
            user_id=account.user_id,
            cash=account.cash,
        )


class AccountResponse(BaseModel):
    result: AccountResponseDTO
