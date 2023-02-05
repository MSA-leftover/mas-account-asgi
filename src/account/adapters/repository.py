from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import Select

from typing import List

from account.domain.entity import Account

from typing import Set


class AbstractRepository(ABC):
    def __init__(self):
        self.seen: Set = set()

    def add(self, aggregate: Account):
        self._add(account=aggregate)
        self.seen.add(aggregate)

    async def get(self, account_number: str):
        account = await self._get(account_number)
        if account:
            self.seen.add(account)
        return account

    async def list_by_userid(self, userid: str) -> List[Account]:
        accounts: List[Account] = await self._list_by_userid(userid=userid)
        if accounts:
            self.seen.update(accounts)
        return accounts

    @abstractmethod
    def _add(self, account: Account):
        raise NotImplementedError

    @abstractmethod
    async def _get(self, account_number: str):
        raise NotImplementedError

    @abstractmethod
    async def _list_by_userid(self, userid: str):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session
        self._base_query: Select = select(Account)

    def _add(self, account: Account):
        self.session.add(account)

    async def _get(self, account_number: str):
        query = await self.session.execute(
            self._base_query.where(
                Account.account_number == account_number
            ).limit(1)
        )
        return query.scalars().first()

    async def _list_by_userid(self, userid: str):
        query = await self.session.execute(
            self._base_query.where(Account.user_id == userid)
        )
        return query.scalars().all()
