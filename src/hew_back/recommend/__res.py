import uuid
from dataclasses import dataclass
from datetime import datetime

import pydantic


@pydantic.dataclasses.dataclass
class GetRecommendRes:
    product_id: uuid.UUID
    product_thumbnail_uuid: uuid.UUID

@dataclass
class ProductRes:
    """製品情報のレスポンスクラス"""
    product_id: uuid.UUID
    product_title: str
    product_thumbnail_uuid: uuid.UUID
    product_contents_uuid: uuid.UUID
    product_price: int
    product_description: str
    purchase_date: datetime.date # ←　いらない？

    @staticmethod
    def create(
            product_id: uuid.UUID,
            product_title: str,
            product_thumbnail_uuid: uuid.UUID,
            product_contents_uuid: uuid.UUID,
            product_price: int,
            product_description: str,
            purchase_date: datetime.date
    ) -> "ProductRes":
        return ProductRes(
            product_id=product_id,
            product_title=product_title,
            product_thumbnail_uuid=product_thumbnail_uuid,
            product_contents_uuid=product_contents_uuid,
            product_price=product_price,
            product_description=product_description,
            purchase_date=purchase_date
        )

