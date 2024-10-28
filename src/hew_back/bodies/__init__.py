import uuid

from pydantic import field_serializer
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls, results, deps
from .__token_bodies import *


class PostUserBody(BaseModel):
    user_name: str
    user_icon_uuid: uuid.UUID | None

    @field_serializer("user_icon_uuid")
    def serialize_sub(self, user_icon_uuid: uuid.UUID) -> str | None:
        if user_icon_uuid is None:
            return None
        return str(user_icon_uuid)

    async def save_new(
            self,
            session: AsyncSession,
            profile: keycloak.KeycloakUserProfile
    ) -> results.UserResult:
        if self.user_icon_uuid is not None:
            mdls.ImagePreferenceRequest.crete(mdls.State.public).post_preference(self.user_icon_uuid)
        # UserTableクラスは、SQLAlchemy を使ってデータベース上のテーブルを定義しており、
        # API から受け取ったデータをデータベースに保存したり、データベースからデータを取得して
        # API に返すための処理を行う。

        # new_record メソッドを使って、新しいユーザーをデータベースに追加
        tbl = tbls.UserTable.create(
            user_id=profile.sub,
            user_name=self.user_name,
            user_screen_id=profile.preferred_username,
            user_icon_uuid=self.user_icon_uuid,
            user_mail=profile.email,
        )
        await tbl.save_new(session)
        await session.commit()
        await session.refresh(tbl)
        return results.UserResult(tbl)


class PostCreatorBody(BaseModel):
    user_id: uuid.UUID
    contact_address: str
    transfer_target: str

    async def save_new(self, user: deps.UserDeps, session: AsyncSession) -> results.CreatorResult:
        creator_table = tbls.CreatorTable.create(user.user_table, self.contact_address, self.transfer_target)
        creator_table.save_new(session)
        await session.commit()
        await session.refresh(creator_table)
        return results.CreatorResult(
            creator_table
        )


class PostChatBody(BaseModel):
    to: uuid.UUID
    message: str
    images: list[uuid.UUID]

    async def save_new(self, user: deps.UserDeps, session: AsyncSession) -> results.ChatResult:
        to_user = await tbls.UserTable.find_one(session, self.to)
        chat = tbls.ChatTable.create(user.user_table, to_user, self.message, session)
        await session.commit()
        await session.refresh(chat)

        images = tbls.ChatImageTable.create_all(chat, self.images, session)
        await session.commit()
        for image in images:
            await session.refresh(image)

        return results.ChatResult(
            chat, images
        )
