import uuid

import pydantic.dataclasses
import sqlalchemy.ext.asyncio
from fastapi import Depends

from hew_back import deps, app, tbls, chat
from hew_back.util import err, Pair


@pydantic.dataclasses.dataclass
class PostColabApproveBody:
    colab_id: uuid.UUID


class Service:
    def __init__(
            self,
            body: PostColabApproveBody,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            sender: deps.CreatorDeps = Depends(deps.CreatorDeps.get),
            chat_service: chat.ChatService = Depends(),
    ):
        self.session = session
        self.sender = sender
        self.body = body
        self.chat_service = chat_service

    async def insert_colab_approve(
            self, colab_creators: list[Pair[tbls.ColabCreatorTable, tbls.CreatorTable]]
    ) -> tbls.ColabApproveTable:
        for colab_creator in colab_creators:
            approve = tbls.ColabApproveTable(colab_creator_id=colab_creator.first.collabo_creator_id)
            self.session.add(approve)
            await self.session.flush()
            await self.session.refresh(approve)
            return approve
        raise err.ErrorIds.INTERNAL_ERROR.to_exception("No colab_creator")

    async def select_owner(self) -> tbls.CreatorTable:
        raw = await self.session.execute(
            sqlalchemy.select(tbls.CreatorTable)
            .join(tbls.ColabTable, tbls.CreatorTable.creator_id == tbls.ColabTable.owner_creator_id)
            .where(tbls.ColabTable.collabo_id == self.body.colab_id)
        )
        return raw.scalar_one()

    async def insert_notification(self, approve: tbls.ColabApproveTable):
        owner = await self.select_owner()
        notification = tbls.NotificationTable(
            receive_user=owner.user_id,
            collabo_approve_id=approve.collabo_approve_id,
        )
        self.session.add(notification)
        await self.session.flush()
        await self.session.refresh(notification)
        return notification

    async def select_colab_creators__creator(self) -> list[Pair[tbls.ColabCreatorTable, tbls.CreatorTable]]:
        raw = await self.session.execute(
            sqlalchemy.select(tbls.ColabCreatorTable, tbls.CreatorTable)
            .select_from(tbls.ColabCreatorTable)
            .distinct()
            .join(tbls.CreatorTable, tbls.CreatorTable.creator_id == tbls.ColabCreatorTable.creator_id)
            .where(tbls.ColabCreatorTable.collabo_id == self.body.colab_id)
        )
        return [Pair(r[0], r[1]) for r in raw.all()]

    async def select_approves(self) -> list[tbls.ColabApproveTable]:
        raw = await self.session.execute(
            sqlalchemy.select(tbls.ColabApproveTable)
            .join(
                tbls.ColabCreatorTable,
                tbls.ColabCreatorTable.collabo_creator_id == tbls.ColabApproveTable.colab_creator_id
            )
            .where(tbls.ColabCreatorTable.collabo_id == self.body.colab_id)
        )
        return [*raw.scalars().all()]

    async def insert_chat_if_everyone_approved(
            self, approves: list[tbls.ColabApproveTable],
            colab_creators: list[Pair[tbls.ColabCreatorTable, tbls.CreatorTable]]
    ):
        approve_creator_colab_ids = [a.colab_creator_id for a in approves]
        for colab_creator in colab_creators:
            if colab_creator.first.collabo_creator_id not in approve_creator_colab_ids:
                return None
        # print(colab_creators)
        await self.chat_service.create_chat([c.second.user_id for c in colab_creators])

    async def process(self):
        colab_creators = self.select_colab_creators__creator()
        approves = await self.select_approves()
        colab_creators = await  colab_creators
        approve = self.insert_colab_approve(colab_creators)
        approve = await approve
        await self.insert_notification(approve)
        await self.insert_chat_if_everyone_approved([*approves, approve], colab_creators)


@app.post("/api/colab/approve")
async def pca(
        service: Service = Depends(),
) -> None:
    return await service.process()
