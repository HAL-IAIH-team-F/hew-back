import uuid

from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls
from hew_back.db import BaseTable


# from asyncpg.pgproto.pgproto import UUID


class CreatorProductTable(BaseTable):
    __tablename__ = 'TBL_CREATOR_PRODUCT'
    creator_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('TBL_PRODUCT.product_id'), primary_key=True, default=uuid.uuid4)

    @staticmethod
    def insert(
            session: AsyncSession,
            creator: tbls.CreatorTable,
            product: tbls.ProductTable,
    ) -> 'CreatorProductTable':
        table = CreatorProductTable(
            creator_id=creator,
            product_id=product,
        )
        session.add(table)
        return table
