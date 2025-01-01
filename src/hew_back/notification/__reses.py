import uuid
from enum import Enum

import pydantic.dataclasses


class NotificationType(Enum):
    COLAB_REQUEST = "colab_request"
    COLAB_APPROVE = "colab_approve"
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
class ColabApproveNotificationData:
    notification_type: NotificationType
    collabo_id: uuid.UUID
    collabo_approve_id: uuid.UUID
    colab_creator_id: str


type NotificationData = ColabNotificationData | ColabRequestNotificationData | ColabApproveNotificationData


@pydantic.dataclasses.dataclass
class NotificationRes:
    notification_id: uuid.UUID
    data: NotificationData
