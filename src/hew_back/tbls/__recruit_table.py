import uuid

import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls
from hew_back.db import BaseTable


class RecruitTable(BaseTable):
    __tablename__ = 'TBL_RECRUIT'  # テーブル名を修正
    recruit_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creator_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CREATOR.creator_id'), nullable=False, default=uuid.uuid4)
    title = Column(String(64), nullable=False)
    description = Column(String(255), nullable=False)
    post_date = Column(sqlalchemy.DateTime, nullable=False, server_default=sqlalchemy.func.now())

    @staticmethod
    def insert(
            session: AsyncSession,
            creator: tbls.CreatorTable,
            title: str,
            description: str,
    ) -> 'RecruitTable':
        table = RecruitTable(
            creator_id=creator.creator_id,
            title=title,
            description=description,
        )
        session.add(table)
        return table
