import datetime

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import table, model
from hew_back.db import DB


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


class SelfUserRes(BaseModel):
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
        return SelfUserRes(
            user_id=user_id,
            user_name=user_name,
            user_screen_id=user_screen_id,
            user_icon_uuid=user_icon_uuid,
            user_date=user_date,
            user_mail=user_mail,
        )

    @staticmethod
    def create_by_user_table(tbl: table.UserTable):
        return SelfUserRes.create(
            user_id=tbl.user_id,
            user_name=tbl.user_name,
            user_screen_id=tbl.user_screen_id,
            user_icon_uuid=tbl.user_icon_uuid,
            user_date=tbl.user_date,
            user_mail=tbl.user_mail,
        )

    @staticmethod
    async def get_self_user_res(
            session: AsyncSession = Depends(DB.get_session),
            token: model.JwtTokenData = Depends(model.JwtTokenData.get_access_token_or_none),
    ):
        tbl = await table.UserTable.find_one(session, token.profile.sub)
        tbl.user_mail = token.profile.email
        tbl.user_screen_id = token.profile.preferred_username
        await session.commit()
        return tbl
