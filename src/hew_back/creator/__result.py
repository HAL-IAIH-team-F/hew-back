from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls
from hew_back.creator.__res import CreatorResponse


@dataclass
class CreatorResult:
    creator: tbls.CreatorTable

    def to_creator_res(self):
        return CreatorResponse(
            creator_id=self.creator.creator_id,
            user_id=self.creator.user_id,
            contact_address=self.creator.contact_address,
        )

    async def refresh(self, session: AsyncSession):
        for wait in [
            session.refresh(self.creator),
        ]:
            await wait
