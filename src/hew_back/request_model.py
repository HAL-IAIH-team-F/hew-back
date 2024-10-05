import uuid

from pydantic import BaseModel

from hew_back import tbls


class SelfCreatorRes(BaseModel):
    creator_id: uuid.UUID
    user_id: uuid.UUID
    contact_address: str

    @staticmethod
    def create(
            creator: tbls.CreatorTable,
            user: tbls.UserTable,
            contact_address: str,
    ):
        return SelfCreatorRes(
            creator_id=creator.creator_id,
            user_id=user.user_id,
            contact_address=contact_address,
        )
