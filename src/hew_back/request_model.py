from pydantic import BaseModel


class PostCreatorBody(BaseModel):

    user:int
    contact_address:str
    transfer_target: str
