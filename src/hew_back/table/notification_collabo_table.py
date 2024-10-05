from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class NotificationCollaboTable(Base):
    __tablename__ = 'TBL_NOTIFICATION_COLLABO'

    collabo_notification_id = Column(String(64), primary_key=False, autoincrement=False)
    notification_id = Column(String(64), ForeignKey('TBL_NOTIFICATION.notification_id'), nullable=False)
    contact_address = Column(String(64), nullable=False)



