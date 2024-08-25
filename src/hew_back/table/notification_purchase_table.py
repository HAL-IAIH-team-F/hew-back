from sqlalchemy import Column, uuid, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NotificationPurchase(Base):
    __tablename__ = 'TBL_NOTIFICATION_PURCHASE'
    purchase_notification_id = Column(uuid.UUID, primary_key=False,default=False)
    notification_id = Column(uuid.UUID, ForeignKey('TBL_NOTIFICATION.id'),nullable=False)
