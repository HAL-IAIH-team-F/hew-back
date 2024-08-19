import datetime

import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from hew_back.db import BaseTable


class UserTable(BaseTable):
    __tablename__ = 'TBL_USER'

    user_id: Mapped[str] = Column(String(64), primary_key=True, autoincrement=False)
    user_name = Column(String(64), nullable=False)
    user_screen_id = Column(String(64), nullable=False, unique=False)
    user_icon_uuid = Column(String(36), nullable=True)
    user_date = Column(DateTime, default=datetime.datetime.now)
    user_mail = Column(String(64), nullable=False, unique=False)

    @staticmethod
    def new_record(
            session: AsyncSession,
            user_id: str,
            user_name: str,
            user_screen_id: str,
            user_icon_uuid: str,
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
