import uuid

from pydantic import BaseModel

class GetRecommendRes(BaseModel):
    product_id: uuid.UUID
    product_thumbnail_uuid: uuid.UUID

    @staticmethod
    def create(
            product_id: uuid.UUID,
            product_thumbnail_uuid: uuid.UUID,
    ):
        return GetRecommendRes(
            product_id=product_id,
            product_thumbnail_uuid=product_thumbnail_uuid,
        )
