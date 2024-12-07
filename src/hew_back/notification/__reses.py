import uuid
from enum import Enum

import pydantic.dataclasses


class NotificationType(Enum):
    COLAB = "colab"


@pydantic.dataclasses.dataclass
class NotificationRes:
    notification_id: uuid.UUID
    notification_type: NotificationType
