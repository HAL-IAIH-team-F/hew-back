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

    async def receiver(self, recruit: tbls.RecruitTable) -> tbls.CreatorTable:
        receiver_creator = await self.session.execute(
            sqlalchemy.select(tbls.CreatorTable)
            .where(tbls.CreatorTable.creator_id == recruit.creator_id)
        )
        return receiver_creator.scalar_one()

    async def insert_notification(self, recruit: tbls.RecruitTable) -> tbls.NotificationTable:
        collabo = await self.insert_colab_notification(recruit)
        receiver = await self.receiver(recruit)
        notification = tbls.NotificationTable(
            receive_user=receiver.user_id,
            collabo_request_id=collabo.collabo_request_id,
        )
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

    async def insert_colab_notification(
            self, recruit: tbls.RecruitTable
    ) -> tbls.ColabRequestTable:
        colab = tbls.ColabRequestTable(
            sender_creator_id=self.sender.creator_table.creator_id,
            receive_creator_id=recruit.creator_id,
        )
        self.session.add(colab)
        await self.session.flush()
        await self.session.refresh(colab)
        return colab

    async def send_request(self):
        recruit = await self.select_recruit()
        await self.insert_notification(recruit)


@app.post("/api/colab/request")
async def pcr(
        service: Service = Depends(),
) -> None:
    return await service.send_request()
