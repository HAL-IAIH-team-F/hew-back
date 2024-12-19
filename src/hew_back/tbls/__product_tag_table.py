import dataclasses
import uuid

from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.orm import Mapped

from hew_back.db import BaseTable


@dataclasses.dataclass
class ProductTag(BaseTable):
    __tablename__ = 'TBL_PRODUCT_TAG'
    item_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey('TBL_PRODUCT.product_id'), primary_key=True,
                                        default=uuid.uuid4)
    tag_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey('TBL_TAG.tag_id'), primary_key=True,
                                       default=uuid.uuid4)
