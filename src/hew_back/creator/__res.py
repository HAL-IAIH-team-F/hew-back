import uuid

import pydantic.dataclasses


@pydantic.dataclasses.dataclass
class CreatorResponse:
    creator_id: uuid.UUID
    user_id: uuid.UUID
    contact_address: str
    transfer_target: str
