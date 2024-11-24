import uuid
from datetime import datetime

from pydantic import field_serializer
from pydantic.dataclasses import dataclass


@dataclass
class PostProductBody:
    price: int
    product_title: str
    product_description: str
    purchase_date: datetime
    product_thumbnail_uuid: uuid.UUID
    product_contents_uuid: uuid.UUID

    @field_serializer("purchase_date")
    def serialize_sub(self, user_date: datetime) -> str:
        return user_date.strftime('%Y-%m-%dT%H:%M:%SZ')
