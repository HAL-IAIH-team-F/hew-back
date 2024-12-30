import dataclasses
import uuid

import pydantic.dataclasses
import sqlalchemy.ext.asyncio
from fastapi import Depends

from hew_back import deps, app, tbls
from hew_back.tbls import CollaboCreatorTable


@pydantic.dataclasses.dataclass
class PostCollaboBody:
    title: str
    description: str
    creators: list[uuid.UUID]


@dataclasses.dataclass
class Record:
    request: tbls.ColabRequestTable


class __Service:
    def __init__(
            self,
            body: PostCollaboBody,
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

    async def select_creators(self) -> list[tbls.CreatorTable]:
        st = await self.session.execute(
            sqlalchemy.select(tbls.CreatorTable)
            .where(tbls.CreatorTable.creator_id.in_(self.body.creators))
        )
        records = st.scalars().all()
        return [*records]

    async def insert_colab(self) -> tbls.ColabTable:
        colab = tbls.ColabTable(
            owner_creator_id=self.sender.creator_table.creator_id,
            title=self.body.title,
            description=self.body.description,
        )
        self.session.add(colab)
        await self.session.flush()
        await self.session.refresh(colab)
        return colab

    async def insert_colab_creators(
            self, creators: list[tbls.CreatorTable], colab: tbls.ColabTable
    ) -> list[CollaboCreatorTable]:
        colab_creators = list[tbls.CollaboCreatorTable]()
        for record in creators:
            colab_creator = tbls.CollaboCreatorTable(
                creator_id=record.creator_id,
                collabo_id=colab.collabo_id,
            )
            self.session.add(colab_creator)
            colab_creators.append(colab_creator)
        await self.session.flush()
        for colab_creator in colab_creators:
            await self.session.refresh(colab_creator)
        return colab_creators

    async def insert_notification(
            self, creators: list[tbls.CreatorTable], colab: tbls.ColabTable
    ):
        notifications = list[tbls.NotificationTable]()
        for creator in creators:
            notification = tbls.NotificationTable(
                receive_user=creator.user_id,
                collabo_id=colab.collabo_id,
            )
            self.session.add(notification)
        await self.session.flush()
        for notification in notifications:
            await self.session.refresh(notification)
        return notifications

    async def process(self):
        colab = await self.insert_colab()
        creators = await self.select_creators()
        await self.insert_colab_creators(creators, colab)
        await self.insert_notification(creators, colab)


@app.post("/api/colab")
async def pc(
        service: __Service = Depends(),
) -> None:
    return await service.process()
