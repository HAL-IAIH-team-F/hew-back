from datetime import datetime

import pydantic
from pydantic import field_serializer

from hew_back import mdls, tbls
from hew_back.mdls import CreatorData, UserData
from hew_back.util.pydanticutl import Uuid


@pydantic.dataclasses.dataclass
class UserRes(UserData):
    creator_data: CreatorData | None

@pydantic.dataclasses.dataclass
class SelfUserRes:
    user_id: Uuid
    user_name: str
    user_screen_id: str
    user_icon: mdls.File | None
    user_date: datetime
    user_mail: str
    creator_data: CreatorData | None

    @field_serializer("user_date")
    def serialize_sub(self, user_date: datetime) -> str:
        return user_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    @staticmethod
    def create_by_user_table(tbl: tbls.UserTable):
        if tbl.user_icon_uuid is None:
            user_icon = None
        else:
            user_icon = mdls.File(
                image_uuid=tbl.user_icon_uuid,
                token=None,
            )
        return SelfUserRes(
            user_id=tbl.user_id,
            user_name=tbl.user_name,
            user_screen_id=tbl.user_screen_id,
            user_icon=user_icon,
            user_date=tbl.user_date,
            user_mail=tbl.user_mail,
        )

