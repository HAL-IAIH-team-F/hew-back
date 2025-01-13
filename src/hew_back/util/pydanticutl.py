import uuid
from datetime import datetime, timezone
from typing import Annotated

from pydantic import AfterValidator, PlainSerializer, PlainValidator


def __validate_datetime(prev: datetime):
    return prev.astimezone(timezone.utc).replace(microsecond=0)


def __serialize_datetime(prev: datetime):
    return prev.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


Datetime = Annotated[
    datetime,
    AfterValidator(__validate_datetime),
    PlainSerializer(__serialize_datetime),
]

def __validate_uuid(prev: str):
    return uuid.UUID(prev)


def __serialize_uuid(prev: uuid.UUID):
    return str(prev)


Uuid = Annotated[
    datetime,
    PlainValidator(__validate_uuid),
    PlainSerializer(__serialize_uuid),
]
