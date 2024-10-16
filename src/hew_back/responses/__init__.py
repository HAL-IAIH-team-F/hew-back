import uuid
from datetime import datetime
from typing import Union
from uuid import UUID

from pydantic import BaseModel, field_serializer
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tables, mdls
from hew_back.util import tks, OrderDirection


# 例:文字列のクエリパラメーターを受け取る
# api → model → table
# 最終的にtableでjoin句などを使用して、product_idなどを返し、それをapiに伝える
# table → model → api

class GetProductsResponse(BaseModel):
    product_text: str
    product_id: UUID
    product_thumbnail_uuid: UUID
    product_price: int
    product_title: str
    product_date: datetime
    product_contents_uuid: UUID



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
            time_order: OrderDirection,
            name_order: OrderDirection,
            like_order: OrderDirection,
            sort: list[str]
    ) -> list["GetProductsResponse"]:
        products_data = await tables.ProductTable.find_products_or_null(
            session=session,
            name=name,
            tag=tag,
            post_by=post_by,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            following=following,
            read_limit_number=read_limit_number,
            time_order=time_order,
            name_order=name_order,
            like_order=like_order,
            sort=sort,
        )



        # Pydanticモデルのリストに変換

        # **は辞書の展開を意味
        # product.__dict__に含まれるキーと値が、GetProductsResponseのフィールドにマッピング
        if products_data:
            return [GetProductsResponse(**product.__dict__) for product in products_data]
        else:
            return []

    class Config:
        from_attributes = True  # SQLAlchemyオブジェクトからPydanticモデルへの変換を有効に



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
    def create_by_user_table(tbl: tables.UserTable):
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
