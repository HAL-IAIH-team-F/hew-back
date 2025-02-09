import uuid

from pydantic.dataclasses import dataclass

from hew_back import mdls
from hew_back.util import pydanticutl


@dataclass
class PostProductBody:
    price: int
    product_title: str
    product_description: str
    purchase_date: pydanticutl.Datetime
    product_thumbnail_uuid: mdls.Uuid
    product_contents_uuid: mdls.Uuid
    collaborator_ids: list[mdls.Uuid]