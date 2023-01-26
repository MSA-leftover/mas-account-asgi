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

    async def get(self, id: str) -> Account:
        account: Account = await self._get(id)
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
    async def _get(self, id: str) -> Account:
        raise NotImplementedError

    @abstractmethod
    async def _list_by_userid(self, userid: str) -> List[Account]:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session
        self._base_query: Select = select(Account)

    def _add(self, account: Account):
        self.session.add(account)

    async def _get(self, id: str) -> Account:
        query = await self.session.execute(
            self._base_query.where(Account.id == id).limit(1)
        )
        return query.scalars().first()

    async def _list_by_userid(self, userid: str) -> List[Account]:
        query = await  self.session.execute(
            self._base_query.where(Account.user_id == userid)
        )
        return query.scalars().all()
