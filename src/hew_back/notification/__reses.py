import uuid
from enum import Enum

import pydantic.dataclasses


class NotificationType(Enum):
    COLAB = "colab"


@pydantic.dataclasses.dataclass
class ColabNotificationData:
    notification_type: NotificationType
    collabo_id: uuid.UUID
    sender_creator_id: uuid.UUID


@pydantic.dataclasses.dataclass
class NotificationRes:
    notification_id: uuid.UUID
    data: ColabNotificationData
