import uuid
from datetime import datetime
from typing import Union
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tables
from hew_back.util import keycloak, tokens


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
        products_fr_tbl = await tables.ProductTable.find_products_or_null(
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
    def create_by_user_table(tbl: tables.UserTable):
        return SelfUserRes.create(
            user_id=tbl.user_id,
            user_name=tbl.user_name,
            user_screen_id=tbl.user_screen_id,
            user_icon_uuid=tbl.user_icon_uuid,
            user_date=tbl.user_date,
            user_mail=tbl.user_mail,
        )


class TokenRes(BaseModel):
    access: tokens.TokenInfo
    refresh: tokens.TokenInfo

    @staticmethod
    def create(access: tokens.TokenInfo, refresh: tokens.TokenInfo):
        return TokenRes(access=access, refresh=refresh)

    @staticmethod
    def create_by_keycloak_user_profile(profile: keycloak.KeycloakUserProfile):
        return TokenRes.create(
            tokens.TokenInfo.create_access_token(profile),
            tokens.TokenInfo.create_refresh_token(profile)
        )


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
