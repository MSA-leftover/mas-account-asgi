from abc import ABC, abstractmethod

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable

from core.infra.database import async_transactional_session
from account.adapters import repository


class AbstractUnitOfWork(ABC):
    repository: repository.AbstractRepository

    async def commit(self):
        await self._commit()

    async def rollback(self):
        await self._rollback()

    def collect_new_events(self):
        for domain_model in self.repository.seen:
            while domain_model.events:
                yield domain_model.events.pop(0)

    @abstractmethod
    async def _commit(self):
        raise NotImplementedError

    @abstractmethod
    async def _rollback(self):
        raise NotImplementedError

    async def __aenter__(self):
        ...

    async def __aexit__(self, *args, **kwargs):
        ...


def DEFAULT_SESSION_FACTORY() -> Callable:
    return async_transactional_session


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=Depends(DEFAULT_SESSION_FACTORY)):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.repository = repository.SqlAlchemyRepository(session=self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args, **kwargs):
        await super().__aexit__(*args)
        await self.session.rollback()
        await self.session.close()

    async def _commit(self):
        await self.session.commit()

    async def _rollback(self):
        await self.session.rollback()
