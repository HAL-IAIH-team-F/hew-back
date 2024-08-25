from sqlalchemy import Column,  String,uuid, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class UserTable(Base):
    __tablename__ = 'TBL_USER'

    user_id = Column(uuid.UUID, primary_key=False, default=False)
    user_name = Column(String(64), nullable=False)
    user_screen_id = Column(String(64), nullable=False, unique=False)
    user_icon_uuid = Column(String(36), nullable=True)
    user_date = Column(DateTime, default=datetime.datetime.now)
    user_mail = Column(String(64), nullable=False, unique=False)



