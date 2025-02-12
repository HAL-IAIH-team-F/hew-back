import pydantic.dataclasses

from hew_back.util.pydanticutl import Uuid


@pydantic.dataclasses.dataclass
class UserBody:
    user_name: str
    user_icon_uuid: Uuid | None
