import uuid

from sqlalchemy import Column, ForeignKey, UUID

from hew_back.db import BaseTable


class ProductTag(BaseTable):
    __tablename__ = 'TBL_PRODUCT_TAG'
    item_id = Column(UUID(as_uuid=True), ForeignKey('TBL_PRODUCT.product_id'), primary_key=True, default=uuid.uuid4)
    tag_id = Column(UUID(as_uuid=True), ForeignKey('TBL_TAG.tag_id'), primary_key=True, default=uuid.uuid4)


# engine = create_engine('sqlite:///purchases.db')
# Base.metadata.create_all(engine)
