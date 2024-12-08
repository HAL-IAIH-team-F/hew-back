import uuid

from pydantic.dataclasses import dataclass


@dataclass
class RecruitRes:
    recruit_id: uuid.UUID
    creator_id: uuid.UUID
    title: str
    description: str
