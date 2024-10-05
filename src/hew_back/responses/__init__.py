import uuid
from datetime import datetime
from typing import Union
from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls, models
from hew_back.db import DB
from hew_back.models import TokenInfo, JwtTokenData
from hew_back.util import keycloak


# 例:文字列のクエリパラメーターを受け取る
# api → model → table
# 最終的にtableでjoin句などを使用して、product_idなどを返し、それをapiに伝える
# table → model → api
class GetProductsResponse(BaseModel):
    # product_id: uuid
    # product_name: str

    @staticmethod
    async def get_products(
            session: AsyncSession,
            name: Union[list[str], None],
            tag: Union[list[str], None],
            post_by: Union[list[UUID], None],
            start_datetime: Union[datetime, None],
            end_datetime: Union[datetime, None],
            following: Union[bool, None],
            read_limit_number: Union[int, None],
    ):
        products_fr_tbl = await tbls.ProductTable.find_products_or_null(
            session=session,
            name=name,
            tag=tag,
            post_by=post_by,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            following=following,
            read_limit_number=read_limit_number
        )
        return products_fr_tbl,  # name, start_datetime, end_datetime, following, read_limit_number, products_fr_tbl


class TokenRes(BaseModel):
    access: TokenInfo
    refresh: TokenInfo

    @staticmethod
    def create(access: TokenInfo, refresh: TokenInfo):
        return TokenRes(access=access, refresh=refresh)

    @staticmethod
    def create_by_jwt_token_data(data: JwtTokenData):
        return TokenRes.create_by_keycloak_user_profile(data.profile)

    @staticmethod
    def create_by_keycloak_user_profile(profile: keycloak.KeycloakUserProfile):
        return TokenRes.create(
            TokenInfo.create_access_token(profile),
            TokenInfo.create_refresh_token(profile)
        )


class SelfUserRes(BaseModel):
    user_id: uuid.UUID
    user_name: str
    user_screen_id: str
    user_icon_uuid: uuid.UUID | None
    user_date: datetime
    user_mail: str

    @staticmethod
    def create(
            user_id: uuid.UUID,
            user_name: str,
            user_screen_id: str,
            user_icon_uuid: uuid.UUID | None,
            user_date: datetime,
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
    def create_by_user_table(tbl: tbls.UserTable):
        return SelfUserRes.create(
            user_id=tbl.user_id,
            user_name=tbl.user_name,
            user_screen_id=tbl.user_screen_id,
            user_icon_uuid=tbl.user_icon_uuid,
            user_date=tbl.user_date,
            user_mail=tbl.user_mail,
        )

    @staticmethod
    async def get_self_user_res_or_none(
            session: AsyncSession = Depends(DB.get_session),
            token: models.JwtTokenData = Depends(models.JwtTokenData.get_access_token_or_none),
    ) -> Union['SelfUserRes', None]:
        tbl = await tbls.UserTable.find_one_or_none(session, token.profile.sub)
        if tbl is None:
            return None
        tbl.user_mail = token.profile.email
        tbl.user_screen_id = token.profile.preferred_username
        res = SelfUserRes.create_by_user_table(tbl)
        await session.commit()
        return res

    @staticmethod
    async def get_self_user_res(
            session: AsyncSession = Depends(DB.get_session),
            token: models.JwtTokenData = Depends(models.JwtTokenData.get_access_token_or_none),
    ):
        tbl = await tbls.UserTable.find_one(session, token.profile.sub)
        tbl.user_mail = token.profile.email
        tbl.user_screen_id = token.profile.preferred_username
        await session.commit()
        return tbl
