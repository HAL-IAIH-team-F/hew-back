import datetime
import uuid
from typing import Union

import sqlalchemy
from sqlalchemy import Column, String, DateTime, UUID
# # from asyncpg.pgproto.pgproto import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from hew_back import error, model
from hew_back.db import BaseTable


class UserTable(BaseTable):
    __tablename__ = 'TBL_USER'

    user_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, autoincrement=False)
    user_name = Column(String(64), nullable=False)
    # アットマーク
    user_screen_id = Column(String(64), nullable=False)
    user_icon_uuid: Mapped[uuid.UUID | None] = Column(UUID(as_uuid=True), nullable=True)
    user_date = Column(DateTime, default=datetime.datetime.now)
    user_mail = Column(String(64), nullable=False, unique=False)

    @staticmethod
    def create(
            session: AsyncSession,
            user_id: uuid.UUID,
            user_name: str,
            user_screen_id: str,
            user_icon_uuid: uuid.UUID | None,
            user_mail: str,
    ):
        tbl = UserTable(
            user_id=user_id,
            user_name=user_name,
            user_screen_id=user_screen_id,
            user_icon_uuid=user_icon_uuid,
            user_mail=user_mail,
        )
        session.add(tbl)
        return tbl

    @staticmethod
    async def find_one_or_none(session: AsyncSession, user_id: uuid.UUID) -> Union['UserTable', None]:
        res = await session.execute(
            sqlalchemy.select(UserTable)
            .where(UserTable.user_id == user_id)
        )
        tbl = res.scalar_one_or_none()
        return tbl

    @staticmethod
    async def find_one(session: AsyncSession, user_id: uuid.UUID) -> 'UserTable':
        tbl = await UserTable.find_one_or_none(session, user_id)
        if tbl is None:
            raise error.ErrorIdException(model.ErrorIds.USER_NOT_FOUND)
        return tbl
