import pydantic
import uuid
import datetime


@pydantic.dataclasses.dataclass
class GetRecommendRes:
    product_id: uuid.UUID
    product_price: int
    product_title: str
    product_description: str
    purchase_date: datetime.datetime
    product_thumbnail_uuid: uuid.UUID
    product_contents_uuid: uuid.UUID
