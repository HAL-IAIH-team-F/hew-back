import uuid

import pydantic.dataclasses
import sqlalchemy.ext.asyncio
from fastapi import Depends

from hew_back import deps, app, tbls
from hew_back.tbls import CollaboApproveTable


@pydantic.dataclasses.dataclass
class PostCollaboApproveBody:
    collabo_id: uuid.UUID


class __Service:
    def __init__(
            self,
            body: PostCollaboApproveBody,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            sender: deps.CreatorDeps = Depends(deps.CreatorDeps.get),
    ):
        self.session = session
        self.sender = sender
        self.body = body

    async def receiver(self, collabo: tbls.ColabRequestTable) -> tbls.CreatorTable:
        receiver_creator = await self.session.execute(
            sqlalchemy.select(tbls.CreatorTable)
            .where(tbls.CreatorTable.creator_id == collabo.sender_creator_id)
        )
        return receiver_creator.scalar_one()

    async def insert_notification(
            self, collabo: tbls.ColabRequestTable,
    ) -> tbls.NotificationTable:
        approve = await self.insert_approve(collabo)
        receiver = await self.receiver(collabo)
        notification = tbls.NotificationTable(
            receive_user=receiver.user_id,
            collabo_approve_id=approve.approve_id,
        )
        self.session.add(notification)
        await self.session.flush()
        await self.session.refresh(notification)
        return notification

    async def select_collabo(self) -> tbls.ColabRequestTable:
        recruit = await self.session.execute(
            sqlalchemy.select(tbls.ColabRequestTable)
            .where(tbls.ColabRequestTable.collabo_id == self.body.collabo_id)
        )
        return recruit.scalar_one()

    async def insert_approve(self, collabo: tbls.ColabRequestTable) -> CollaboApproveTable:
        colab = tbls.CollaboApproveTable(
            collabo_id=collabo.collabo_id,
        )
        self.session.add(colab)
        await self.session.flush()
        await self.session.refresh(colab)
        return colab

    async def update_notification(self, collabo: tbls.ColabRequestTable):
        query = await self.session.execute(
            sqlalchemy.select(tbls.NotificationTable)
            .where(tbls.NotificationTable.collabo_id == collabo.collabo_id)
        )
        collabo_notification: tbls.NotificationTable = query.scalar_one()
        collabo_notification.read = True

    async def approve(self):
        collabo = await self.select_collabo()
        await self.update_notification(collabo)
        await self.insert_notification(collabo)


@app.post("/api/colab/approve")
async def pca(
        service: __Service = Depends(),
) -> None:
    return await service.approve()
