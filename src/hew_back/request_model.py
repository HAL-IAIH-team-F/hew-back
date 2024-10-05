import uuid

from pydantic import BaseModel

from hew_back import tables


class SelfCreatorRes(BaseModel):
    creator_id: uuid.UUID
    user_id: uuid.UUID
    contact_address: str

    @staticmethod
    def create(
            creator: tables.CreatorTable,
            user: tables.UserTable,
            contact_address: str,
    ):
        return SelfCreatorRes(
            creator_id=creator.creator_id,
            user_id=user.user_id,
            contact_address=contact_address,
        )
