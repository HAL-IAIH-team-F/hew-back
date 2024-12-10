import uuid
from typing import Union

import sqlalchemy
from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from hew_back import tbls
from hew_back.db import BaseTable
from hew_back.util import err


class CreatorTable(BaseTable):
    __tablename__ = 'TBL_CREATOR'  # テーブル名の修正
    creator_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey('TBL_USER.user_id'), nullable=False, unique=True,
    )
    contact_address = Column(String(64), nullable=False)
    transfer_target = Column(String(64), nullable=False)  # 振込先

    @staticmethod
    async def find_one_or_none_by_user_id(
            session: AsyncSession,
            user_id: uuid.UUID
    ) -> Union['CreatorTable', None]:
        res = await session.execute(
            sqlalchemy.select(CreatorTable)
            .where(CreatorTable.user_id == user_id)
        )
        tbl = res.scalar_one_or_none()
        return tbl

    @staticmethod
    async def find_one(session: AsyncSession, user_id: uuid.UUID) -> 'CreatorTable':
        tbl = await CreatorTable.find_one_or_none_by_user_id(session, user_id)
        if tbl is None:
            raise err.ErrorIdException(err.ErrorIds.CREATOR_NOT_FOUND)
        return tbl

    def save_new(self, session: AsyncSession):
        session.add(self)

    @staticmethod
    def create(
            user: tbls.UserTable,
            contact_address: str,
            transfer_target: str,
    ) -> 'CreatorTable':
        return CreatorTable(
            user_id=user.user_id,
            contact_address=contact_address,
            transfer_target=transfer_target,
        )
