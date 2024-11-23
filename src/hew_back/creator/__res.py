import uuid

from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls


class CreatorResponse(BaseModel):
    creator_id: uuid.UUID
    user_id: uuid.UUID
    contact_address: str
    transfer_target: str

    @staticmethod
    def create(
            creator_id: uuid.UUID,
            user_id: uuid.UUID,
            contact_address: str,
            transfer_target: str,
    ) -> 'CreatorResponse':
        return CreatorResponse(
            creator_id=creator_id,
            user_id=user_id,
            contact_address=contact_address,
            transfer_target=transfer_target,
        )

class RecruitCreator(BaseModel):
    creator_recruit_id: uuid.UUID
    creator_id: uuid.UUID
    contact_address: str
    title: str
    context:str

    @staticmethod
    async def recruit_creator(
        session: AsyncSession,
        user_id: uuid.UUID,
    ) -> 'RecruitCreator':
        result = await tbls.CreatorRecruitTable.post_recruit_creator(
            session=session,
            user_id=user_id,
        )

        # resultの加工
        # return result
