import datetime

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import table, model


class PostUserBody(BaseModel):
    user_name: str

    def new_record(
            self,
            session: AsyncSession,
            profile: model.KeycloakUserProfile
    ):
        tbl = table.UserTable.new_record(
            session=session,
            user_id=profile.sub,
            user_name=self.user_name,
            user_screen_id=profile.preferred_username,
            user_icon_uuid="",
            user_mail=profile.email,
        )
        return tbl


class UserRes(BaseModel):
    user_id: str
    user_name: str
    user_screen_id: str
    user_icon_uuid: str
    user_date: datetime.datetime
    user_mail: str

    @staticmethod
    def create(
            user_id: str,
            user_name: str,
            user_screen_id: str,
            user_icon_uuid: str,
            user_date: datetime.datetime,
            user_mail: str,
    ):
        return UserRes(
            user_id=user_id,
            user_name=user_name,
            user_screen_id=user_screen_id,
            user_icon_uuid=user_icon_uuid,
            user_date=user_date,
            user_mail=user_mail,
        )

    @staticmethod
    def create_by_user_table(tbl: table.UserTable):
        return UserRes.create(
            user_id=tbl.user_id,
            user_name=tbl.user_name,
            user_screen_id=tbl.user_screen_id,
            user_icon_uuid=tbl.user_icon_uuid,
            user_date=tbl.user_date,
            user_mail=tbl.user_mail,
        )
