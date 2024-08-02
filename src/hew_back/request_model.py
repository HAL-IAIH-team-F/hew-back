from pydantic import BaseModel


class PostCreatorBody(BaseModel):
    user_id: int
    contact_address: str
    transfer_target: str
