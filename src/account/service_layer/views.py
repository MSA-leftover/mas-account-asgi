from fastapi import Depends

from account.service_layer import uow


class Views:
    def __init__(
            self,
            uow: uow.AbstractUnitOfWork = Depends(uow.SqlAlchemyUnitOfWork)
    ):
        self.uow = uow

    async def get_account_by_account_number(self, account_number: str):
        async with self.uow:
            result = await self.uow.repository.get(account_number)
            await self.uow.commit()

        return result

    async def is_valid_account_for_amount(
            self, account_number: str, amount: int
    ):
        async with self.uow:
            account = await self.uow.repository.get(account_number)
            await self.uow.commit()

        if account is None:
            return None

        if account.cash < amount:
            return (False, account)

        return (True, account)
