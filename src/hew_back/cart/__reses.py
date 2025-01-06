import uuid
from datetime import datetime

import pydantic.dataclasses


@pydantic.dataclasses.dataclass
class CartRes:
    product_id: uuid.UUID
    product_price: int
    product_title: str
    product_description: str
    purchase_date: datetime
    product_contents_uuid: uuid.UUID
    product_thumbnail_uuid: uuid.UUID
