import uuid

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import deps, tbls
from hew_back.creator.__result import CreatorResult


class PostCreatorBody(BaseModel):
    contact_address: str
    transfer_target: str

    async def save_new(self, user: deps.UserDeps, session: AsyncSession) -> CreatorResult:
        creator_table = tbls.CreatorTable.create(user.user_table, self.contact_address, self.transfer_target)
        creator_table.save_new(session)
        await session.flush()
        await session.refresh(creator_table)
        return CreatorResult(
            creator_table
        )

