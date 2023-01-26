from sqlalchemy import Column, DateTime, MetaData, String, Integer, Table
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import registry, relationship

from account.domain.entity import User, Account
from account.domain.vo import History

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

histories = Table(
    'histories',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('type', String('10')),
    Column('amount', Integer),
    Column('account_number', String('36')),
    Column('other_account_number', String('36'), nullable=False),
    Column('created_at', DateTime(timezone=True), server_default=func.now()),
)


async def account_mapper(engine):
    histories_mapper = mapper_registry.map_imperatively(
        History,
        histories,
        eager_defaults=True,
    )
    mapper_registry.map_imperatively(
        Account,
        accounts,
        eager_defaults=True,
        properties={'histories': relationship(histories_mapper, back_populates='account_number')}
    )

    async with engine.connect() as conn:
        async with conn.begin():
            await conn.run_sync(metadata.create_all)
