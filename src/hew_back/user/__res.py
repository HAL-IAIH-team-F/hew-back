import pydantic

from hew_back import mdls
from hew_back.mdls import CreatorData, UserData
from hew_back.util.pydanticutl import Uuid, Datetime


@pydantic.dataclasses.dataclass
class UserRes(UserData):
    creator_data: CreatorData | None


@pydantic.dataclasses.dataclass
class SelfUserRes:
    user_id: Uuid
    user_name: str
    user_screen_id: str
    user_icon: mdls.File | None
    user_date: Datetime
    user_mail: str
    creator_data: CreatorData | None
