import sqlalchemy
from sqlalchemy import Column, UUID, ForeignKey

from hew_back.db import BaseTable


class CartProductTable(BaseTable):
    __tablename__ = 'TBL_CART_PRODUCT'

    cart_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CART.cart_id'), primary_key=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey('TBL_PRODUCT.product_id'), primary_key=True)

    removed = Column(sqlalchemy.Boolean, default=False)
