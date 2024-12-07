import uuid
from typing import Union, Sequence

import pydantic.dataclasses
import sqlalchemy.ext.asyncio
from fastapi import Depends, Query
from sqlalchemy import ColumnElement

from hew_back import deps, app, tbls
from hew_back.tbls import RecruitTable


def search_stmt(
        name: Union[list[str], None] = Query(default=None),
) -> ColumnElement[bool]:
    if name is None or len(name) == 0:
        return sqlalchemy.true()
    return sqlalchemy.and_(
        *[sqlalchemy.or_(
            RecruitTable.title.like(f"%{keyword}%"),
            RecruitTable.description.like(f"%{keyword}%"),
        ) for keyword in name]
    )


async def find_recruits(
        search: ColumnElement[bool] = Depends(search_stmt),
        limit: Union[int, None] = Query(default=20),
) -> Sequence[RecruitTable]:
    result = await session.execute(
        sqlalchemy.select(RecruitTable)
        .where(search)
        .limit(limit)
    )
    result = result.scalars().all()
    await session.flush()
    for recruit in result:
        await session.refresh(recruit)
    return result


@pydantic.dataclasses.dataclass
class PostColabRequestBody:
    recruit_id: uuid.UUID


@pydantic.dataclasses.dataclass
class __Service:
    def __init__(
            self,
            body: PostColabRequestBody,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            sender: deps.CreatorDeps = Depends(deps.CreatorDeps.get),
    ):
        self.session = session
        self.sender = sender
        self.body = body

    async def insert_notification(self) -> tbls.NotificationTable:
        notification = tbls.NotificationTable()
        self.session.add(notification)
        await self.session.refresh(notification)
        return notification

    async def select_recruit(self) -> tbls.RecruitTable:
        recruit = await self.session.execute(
            sqlalchemy.select(tbls.RecruitTable)
            .where(tbls.RecruitTable.recruit_id == self.body.recruit_id)
        )
        return recruit.scalar_one()

    async def insert_colab_notification(self) -> tbls.NotificationCollaboTable:
        notification = await self.insert_notification()
        recruit = await self.select_recruit()
        colab = tbls.NotificationCollaboTable(
            notification_id=notification.notification_id,
            sender_creator_id=self.sender.creator_table.creator_id,
            receive_creator_id=recruit.creator_id,
        )
        return colab

    async def send_request(self):
        await self.insert_colab_notification()


@app.post("/api/colab/request")
async def pcr(
        service: __Service = Depends(__Service),
) -> None:
    await service.send_request()
    return
