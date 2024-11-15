from sqlalchemy.ext.asyncio import AsyncSession

from hew_back.db import DB


class DbDeps:
    @staticmethod
    async def session() -> AsyncSession:
        async with DB.session_maker() as session:
            yield session
            session.commit()

