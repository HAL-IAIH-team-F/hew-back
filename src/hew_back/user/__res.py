import uuid
from datetime import datetime

from pydantic import BaseModel, field_serializer

from hew_back import mdls, tbls


class SelfUserRes(BaseModel):
    user_id: uuid.UUID
    user_name: str
    user_screen_id: str
    user_icon: mdls.File | None
    user_date: datetime
    user_mail: str

    @field_serializer("user_date")
    def serialize_sub(self, user_date: datetime) -> str:
        return user_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    @staticmethod
    def create(
            user_id: uuid.UUID,
            user_name: str,
            user_screen_id: str,
            user_icon: mdls.File | None,
            user_date: datetime,
            user_mail: str,
    ):
        return SelfUserRes(
            user_id=user_id,
            user_name=user_name,
            user_screen_id=user_screen_id,
            user_icon=user_icon,
            user_date=user_date,
            user_mail=user_mail,
        )

    @staticmethod
    def create_by_user_table(tbl: tbls.UserTable):
        if tbl.user_icon_uuid is None:
            user_icon = None
        else:
            user_icon = mdls.File(
                image_uuid=tbl.user_icon_uuid,
                token=None,
            )
        return SelfUserRes.create(
            user_id=tbl.user_id,
            user_name=tbl.user_name,
            user_screen_id=tbl.user_screen_id,
            user_icon=user_icon,
            user_date=tbl.user_date,
            user_mail=tbl.user_mail,
        )
