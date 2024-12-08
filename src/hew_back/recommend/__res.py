import uuid

import pydantic


@pydantic.dataclasses.dataclass
class GetRecommendRes:
    product_id: uuid.UUID
    product_thumbnail_uuid: uuid.UUID



