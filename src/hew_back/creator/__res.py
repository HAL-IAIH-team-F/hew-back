import uuid

from pydantic import BaseModel


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
