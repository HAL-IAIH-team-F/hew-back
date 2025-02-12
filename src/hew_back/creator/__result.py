from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls


@dataclass
class CreatorResult:
    creator: tbls.CreatorTable

    async def refresh(self, session: AsyncSession):
        for wait in [
            session.refresh(self.creator),
        ]:
            await wait
