import uuid

from pydantic import BaseModel, field_serializer
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import  mdls, tbls
from hew_back.user.__result import UserResult
from hew_back.util import keycloak


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
    ) -> UserResult:
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
        return UserResult(tbl)
