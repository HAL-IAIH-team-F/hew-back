import uuid

import pydantic.dataclasses


@pydantic.dataclasses.dataclass
class CartRes:
    cart_id: uuid.UUID
    user_id: uuid.UUID
    product_ids: list[uuid.UUID]
