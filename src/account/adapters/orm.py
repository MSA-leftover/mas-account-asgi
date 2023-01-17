from sqlalchemy import Column, DateTime, MetaData, String, Integer, Table
from sqlalchemy.orm import registry
from sqlalchemy.sql import func

from account.domain.entity import Account

metadata = MetaData()
mapper_registry = registry(metadata=metadata)

accounts = Table(
    "accounts",
    mapper_registry.metadata,
    Column("id", String(36), primary_key=True),
    Column("name", String(32)),
    Column("user_id", String(36)),
    Column("amount", Integer),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    ),
    Column("deleted_at", DateTime(timezone=True)),
)


def account_mapper():
    mapper_registry.map_imperatively(
        Account,
        accounts,
        eager_defaults=True,
    )
