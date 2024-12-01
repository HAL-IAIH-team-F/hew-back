import uuid
from datetime import datetime
from typing import Union
from uuid import UUID

from pydantic import BaseModel, field_serializer
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls, mdls
from hew_back.util import tks, OrderDirection


class SelfUserRes(BaseModel):
    user_id: uuid.UUID
    user_name: str
    user_screen_id: str
    user_icon: mdls.Img | None
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
            user_icon: mdls.Img | None,
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
            user_icon = mdls.Img.create(tbl.user_icon_uuid, None)
        return SelfUserRes.create(
            user_id=tbl.user_id,
            user_name=tbl.user_name,
            user_screen_id=tbl.user_screen_id,
            user_icon=user_icon,
            user_date=tbl.user_date,
            user_mail=tbl.user_mail,
        )


class TokenRes(BaseModel):
    access: tks.TokenInfo
    refresh: tks.TokenInfo

    @staticmethod
    def from_tokens(tokens: mdls.Tokens):
        return TokenRes.create(tokens.access, tokens.refresh)

    @staticmethod
    def create(access: tks.TokenInfo, refresh: tks.TokenInfo):
        return TokenRes(access=access, refresh=refresh)


class ImgTokenRes(BaseModel):
    upload: tks.TokenInfo

    @staticmethod
    def from_img_tokens(tokens: mdls.ImgTokens):
        return ImgTokenRes.create(tokens.upload)

    @staticmethod
    def create(upload: tks.TokenInfo):
        return ImgTokenRes(upload=upload)


class CreatorResponse(BaseModel):
    creator_id: uuid.UUID
    user_id: uuid.UUID
    contact_address: str
    transfer_target: str

    @staticmethod
    def create(
            creator_id: uuid.UUID,
            user_id: uuid.UUID,
            contact_address: str,
            transfer_target: str,
    ) -> 'CreatorResponse':
        return CreatorResponse(
            creator_id=creator_id,
            user_id=user_id,
            contact_address=contact_address,
            transfer_target=transfer_target,
        )
