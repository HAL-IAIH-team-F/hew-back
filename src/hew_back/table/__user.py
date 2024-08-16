import datetime

from sqlalchemy import Column, String, DateTime

from hew_back.db import BaseTable


class UserTable(BaseTable):
    __tablename__ = 'TBL_USER'

    user_id = Column(String(64), primary_key=False, autoincrement=False)
    user_name = Column(String(64), nullable=False)
    user_screen_id = Column(String(64), nullable=False, unique=False)
    user_icon_uuid = Column(String(36), nullable=True)
    user_date = Column(DateTime, default=datetime.datetime.now)
    user_mail = Column(String(64), nullable=False, unique=False)
