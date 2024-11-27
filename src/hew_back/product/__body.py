import uuid

from pydantic.dataclasses import dataclass

from hew_back import mdls


@dataclass
class PostProductBody:
    price: int
    product_title: str
    product_description: str
    purchase_date: mdls.Datetime
    product_thumbnail_uuid: uuid.UUID
    product_contents_uuid: uuid.UUID
