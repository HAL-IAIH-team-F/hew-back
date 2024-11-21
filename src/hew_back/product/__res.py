import uuid
from datetime import datetime

from pydantic import BaseModel, field_serializer


# 例:文字列のクエリパラメーターを受け取る
# api → model → table
# 最終的にtableでjoin句などを使用して、product_idなどを返し、それをapiに伝える
# table → model → api

class GetProductsResponse(BaseModel):
    product_description: str
    product_id: uuid.UUID
    product_thumbnail_uuid: uuid.UUID
    product_price: int
    product_title: str
    product_date: datetime
    product_contents_uuid: uuid.UUID

    # @field_serializer("sub")
    # def serialize_sub(self, sub: uuid.UUID) -> str:
    #     return str(sub)

    @staticmethod
    def create(
            product_description: str,
            product_id: uuid.UUID,
            product_thumbnail_uuid: uuid.UUID,
            product_price: int,
            product_title: str,
            listing_date: datetime,
            product_contents_uuid: uuid.UUID,
    ) -> "GetProductsResponse":
        return GetProductsResponse(
            product_description=product_description,
            product_id=product_id,
            product_thumbnail_uuid=product_thumbnail_uuid,
            product_price=product_price,
            product_title=product_title,
            product_date=listing_date,
            product_contents_uuid=product_contents_uuid,
        )

    class Config:
        from_attributes = True  # SQLAlchemyオブジェクトからPydanticモデルへの変換を有効に


class ProductRes(BaseModel):
    product_id: uuid.UUID
    product_price: int
    product_title: str
    product_description: str
    listing_date: datetime
    product_thumbnail_uuid: uuid.UUID
    product_contents_uuid: uuid.UUID
    creator_id: uuid.UUID

    @staticmethod
    def create(
            product_id: uuid.UUID,
            product_price: int,
            product_title: str,
            product_description: str,
            listing_date: datetime,
            product_thumbnail_uuid: uuid.UUID,
            product_contents_uuid: uuid.UUID,
            creator_id: uuid.UUID,
    ):
        return ProductRes(
            product_id=product_id,
            product_price=product_price,
            product_title=product_title,
            product_description=product_description,
            listing_date=listing_date,
            product_thumbnail_uuid=product_thumbnail_uuid,
            product_contents_uuid=product_contents_uuid,
            creator_id=creator_id,
        )
