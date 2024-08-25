from sqlalchemy import Column, uuid, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class NotificationCollaboTable(Base):
    __tablename__ = 'TBL_NOTIFICATION_COLLABO'

    collabo_notification_id = Column(uuid.UUID, primary_key=False, default=False)
    notification_id = Column(uuid.UUID, ForeignKey('TBL_NOTIFICATION.notification_id'), nullable=False)
    contact_address = Column(uuid.UUID, nullable=False)



