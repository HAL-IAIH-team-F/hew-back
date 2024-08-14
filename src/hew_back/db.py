from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from hew_back.env import ENV


class Db:
    def __init__(self):
        self.engine = create_async_engine(ENV.database.db_url, echo=False, pool_pre_ping=True)
        self.session_maker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession
        )

    async def get_session(self):
        async with self.session_maker() as session:
            yield session


DB = Db()
BaseTable = declarative_base()
