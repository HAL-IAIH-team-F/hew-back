from pydantic.dataclasses import dataclass

from hew_back.util import pydanticutl
from hew_back.util.pydanticutl import Uuid


@dataclass
class PostProductBody:
    price: int
    product_title: str
    product_description: str
    purchase_date: pydanticutl.Datetime
    product_thumbnail_uuid: Uuid
    product_contents_uuid: Uuid
    collaborator_ids: list[Uuid]
