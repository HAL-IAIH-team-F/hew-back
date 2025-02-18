from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from hew_back.db import DB


class DbDeps:
    @staticmethod
    async def session() -> AsyncGenerator[Any, Any]:
        async with DB.session_maker() as session:
            yield session
            await session.commit()

