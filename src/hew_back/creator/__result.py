from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls
from hew_back.creator.__res import CreatorResponse
from hew_back.mdls import UserData


@dataclass
class CreatorResult:
    creator: tbls.CreatorTable

    async def refresh(self, session: AsyncSession):
        for wait in [
            session.refresh(self.creator),
        ]:
            await wait
