import uuid
from enum import Enum

import pydantic.dataclasses


class NotificationType(Enum):
    COLAB = "colab"
    COLAB_APPROVE = "colab_approve"


@pydantic.dataclasses.dataclass
class CollaboNotificationData:
    notification_type: NotificationType
    collabo_id: uuid.UUID
    sender_creator_id: uuid.UUID

@pydantic.dataclasses.dataclass
class CollaboApproveNotificationData:
    notification_type: NotificationType
    collabo_id: uuid.UUID
    approve_id: uuid.UUID


@pydantic.dataclasses.dataclass
class NotificationRes:
    notification_id: uuid.UUID
    data: CollaboNotificationData | CollaboApproveNotificationData
