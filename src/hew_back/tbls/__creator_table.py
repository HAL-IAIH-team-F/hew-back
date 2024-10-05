import uuid

from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from hew_back import tbls
from hew_back.db import BaseTable


class CreatorTable(BaseTable):
    __tablename__ = 'TBL_CREATOR'  # テーブル名の修正
    creator_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), ForeignKey('TBL_USER.user_id'), nullable=False)
    contact_address = Column(String(64), nullable=False)
    transfer_target = Column(String(64), nullable=False)

    def save(self, session: AsyncSession):
        session.add(self)

    @staticmethod
    def create(
            user: tbls.UserTable,
            contact_address: str,
            transfer_target: str,
    ):
        return CreatorTable(
            user_id=user.user_id,
            contact_address=contact_address,
            transfer_target=transfer_target,
        )
