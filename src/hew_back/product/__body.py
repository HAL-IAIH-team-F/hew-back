import uuid

from pydantic.dataclasses import dataclass

from hew_back.util import pydanticutl


@dataclass
class PostProductBody:
    price: int
    product_title: str
    product_description: str
    purchase_date: pydanticutl.Datetime
    product_thumbnail_uuid: uuid.UUID
    product_contents_uuid: uuid.UUID
    collaborator_ids: list[uuid.UUID]