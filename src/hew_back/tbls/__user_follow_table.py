import uuid

from sqlalchemy import Column, ForeignKey, UUID

from hew_back.db import BaseTable


class UserFollowTable(BaseTable):
    __tablename__ = 'TBL_USER_FOLLOW'
    follow_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('TBL_USER.user_id'), nullable=False)
    creator_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), nullable=False)
