import uuid

import pydantic.dataclasses
import sqlalchemy.ext.asyncio
from fastapi import Depends

from hew_back import deps, app, tbls


@pydantic.dataclasses.dataclass
class PostCollaboGroupBody:
    collabo_id: uuid.UUID
    approves: list[uuid.UUID]


class __Service:
    def __init__(
            self,
            body: PostCollaboGroupBody,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            sender: deps.CreatorDeps = Depends(deps.CreatorDeps.get),
    ):
        self.session = session
        self.sender = sender
        self.body = body

    async def receiver(self, collabo: tbls.CollaboTable) -> tbls.CreatorTable:
        receiver_creator = await self.session.execute(
            sqlalchemy.select(tbls.CreatorTable)
            .where(tbls.CreatorTable.creator_id == collabo.sender_creator_id)
        )
        return receiver_creator.scalar_one()

    async def select_approves(self)->list[tbls.CollaboApproveTable]:
        st = await self.session.execute(
            sqlalchemy.select(tbls.CollaboApproveTable)
            .where(tbls.CollaboApproveTable.approve_id.in_(self.body.approves))
        )
        records = st.scalars().all()
        return [record for record in records]

    async def insert_colab_creators(
            self,
    ) -> tbls.NotificationTable:
        approves =await self.select_approves()
        for approve in approves:
            tbls.CollaboCreatorTable(
                creator_id=approve
            )

        notification = tbls.CollaboCreatorTable(
        )
        self.session.add(notification)
        await self.session.flush()
        await self.session.refresh(notification)
        return notification

    async def process(self):
        await self.insert_colab_creators()


@app.post("/api/colab/approve")
async def pca(
        service: __Service = Depends(),
) -> None:
    return await service.process()
