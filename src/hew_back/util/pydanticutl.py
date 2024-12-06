from datetime import datetime, timezone
from typing import Annotated

from pydantic import AfterValidator, PlainSerializer


def __validate_datetime(prev: datetime):
    return prev.astimezone(timezone.utc).replace(tzinfo=None, microsecond=0)


def __serialize_datetime(prev: datetime):
    return prev.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


Datetime = Annotated[
    datetime,
    AfterValidator(__validate_datetime),
    PlainSerializer(__serialize_datetime),
]
