import pydantic

from hew_back.mdls import CreatorData, UserData
from hew_back.util.pydanticutl import Datetime


@pydantic.dataclasses.dataclass
class UserRes(UserData):
    creator_data: CreatorData | None


@pydantic.dataclasses.dataclass
class SelfUserRes(UserData):
    register_date: Datetime
    user_mail: str
    creator_data: CreatorData | None
