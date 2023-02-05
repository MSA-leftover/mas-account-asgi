from pydantic import BaseModel


class AccountRequest(BaseModel):
    account_number: str


class ValidateAccountRequest(BaseModel):
    account_number: str
    amount: int
