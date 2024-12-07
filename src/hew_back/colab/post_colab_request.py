import uuid

import pydantic.dataclasses
import sqlalchemy.ext.asyncio
from fastapi import Depends

from hew_back import deps, app, tbls


@pydantic.dataclasses.dataclass
class PostColabRequestBody:
    recruit_id: uuid.UUID


class Service:
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
        await self.session.flush()
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
        self.session.add(colab)
        await self.session.flush()
        await self.session.refresh(colab)
        return colab

    async def send_request(self):
        await self.insert_colab_notification()


@app.post("/api/colab/request")
async def pcr(
        service: Service = Depends(),
) -> None:
    await service.send_request()
    return
