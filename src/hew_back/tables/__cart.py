from pygments.lexer import default

from hew_back.db import BaseTable
from sqlalchemy.ext.asyncio import AsyncSession

import uuid
from typing import Union

from fastapi import Query

from sqlalchemy import Column, UUID, Boolean, ForeignKey, select, update, DateTime

from hew_back import tables

class CartTable(BaseTable):
    __tablename__ = 'TBL_CART'

    cart_id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('TBL_USER.user_id'))
    purchase_date = Column(DateTime,  nullable=True)