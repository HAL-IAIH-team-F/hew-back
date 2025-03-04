import uuid

import pydantic.dataclasses

from hew_back.product.__res import ProductRes


@pydantic.dataclasses.dataclass
class CartRes:
    cart_id: uuid.UUID
    user_id: uuid.UUID
    product_ids: list[ProductRes]

