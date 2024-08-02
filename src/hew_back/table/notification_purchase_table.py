from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NotificationPurchase(Base):
    __tablename__ = 'TBL_NOTIFICATION_PURCHASE'
    purchase_notification_id = Column(String(64), primary_key=False)
    notification_id = Column(String(64), ForeignKey('notification.id'),nullable=False)
