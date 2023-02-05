from sqlalchemy.ext.asyncio import \
    AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import settings

engine: AsyncEngine | None = None

DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(
    settings.db_protocol,
    settings.db_user,
    settings.db_password,
    settings.db_host,
    settings.db_port,
    settings.db_name,
)

engine = create_async_engine(DATABASE_URI, future=True)

async_transactional_session: sessionmaker = sessionmaker(
    engine,  # type: ignore
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)
