import uuid
from xml.dom import UserDataHandler

import pydantic.dataclasses

from hew_back.mdls import UserData


@pydantic.dataclasses.dataclass
class CreatorResponse:
    creator_id: uuid.UUID
    contact_address: str
    user_data: UserData