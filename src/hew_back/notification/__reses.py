import uuid
from enum import Enum

import pydantic.dataclasses


class NotificationType(Enum):
    COLAB_REQUEST = "colab_request"
    COLAB = "colab"


@pydantic.dataclasses.dataclass
class ColabRequestNotificationData:
    notification_type: NotificationType
    colab_request_id: uuid.UUID
    from_creator_id: uuid.UUID


@pydantic.dataclasses.dataclass
class ColabNotificationData:
    notification_type: NotificationType
    collabo_id: uuid.UUID
    owner_id: uuid.UUID
    title: str
    description: str
    creator_ids: list[uuid.UUID]


@pydantic.dataclasses.dataclass
class NotificationRes:
    notification_id: uuid.UUID
    data: ColabRequestNotificationData | ColabNotificationData
