from hew_back.db import BaseTable

import uuid


from sqlalchemy import Column, UUID, ForeignKey, DateTime

from hew_back import tbls

class CartTable(BaseTable):
    __tablename__ = 'TBL_CART'

    cart_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('TBL_USER.user_id'))
    purchase_date = Column(DateTime,  nullable=True)