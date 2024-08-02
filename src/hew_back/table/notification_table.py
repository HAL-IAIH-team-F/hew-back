from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class NotificationTable(Base):
    __tablename__ = 'TBL_NOTIFICATION'

    notification_id = Column(String(64), primary_key=True, autoincrement=False)
    destination_id = Column(String(64), ForeignKey('TBL_USER.user_id'), nullable=False)
    sender_id = Column(String(64), ForeignKey('TBL_USER.user_id'), nullable=False)



