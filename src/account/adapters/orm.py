from sqlalchemy import \
    Column, DateTime, MetaData, String, Integer, Table, event
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import registry

from account.domain.entity import Account

metadata = MetaData()
mapper_registry = registry(metadata=metadata)

Base = declarative_base()

accounts = Table(
    'accounts',
    mapper_registry.metadata,
    Column('account_number', String(36), primary_key=True),
    Column('user_id', String(36)),
    Column('name', String(32)),
    Column('cash', Integer),
    Column('created_at', DateTime(timezone=True), server_default=func.now()),
    Column(
        'updated_at',
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    ),
    Column('deleted_at', DateTime(timezone=True)),
)


async def account_mapper(engine):
    mapper_registry.map_imperatively(
        Account,
        accounts,
        eager_defaults=True,
    )

    async with engine.connect() as conn:
        async with conn.begin():
            await conn.run_sync(metadata.create_all)


@event.listens_for(Account, 'load')
def receive_load(account, _):
    account.events = []
