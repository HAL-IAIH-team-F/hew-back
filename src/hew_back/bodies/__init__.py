import uuid
from datetime import datetime, timezone, timedelta

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import ENV, tables, results, deps, models
from hew_back.util import keycloak, tokens


class PostTokenBody(BaseModel):
    keycloak_token: str

    def fetch_keycloak_profile(self) -> keycloak.KeycloakUserProfile:
        well_known = keycloak.WellKnown.fetch(ENV.keycloak.well_known_url)
        return keycloak.KeycloakUserProfile.fetch(well_known, self.keycloak_token)

    def new_tokens(self):
        profile = self.fetch_keycloak_profile()
        return models.Tokens(
            access=models.JwtTokenData.new(
                tokens.TokenType.upload,
                profile
            ).new_token_info(),
            refresh=models.JwtTokenData.new(
                tokens.TokenType.upload,
                profile
            ).new_token_info()
        )


class PostUserBody(BaseModel):
    user_name: str
    user_icon_uuid: uuid.UUID | None

    async def save_new(
            self,
            session: AsyncSession,
            profile: keycloak.KeycloakUserProfile
    ) -> results.UserModel:
        # UserTableクラスは、SQLAlchemy を使ってデータベース上のテーブルを定義しており、
        # API から受け取ったデータをデータベースに保存したり、データベースからデータを取得して
        # API に返すための処理を行う。

        # new_record メソッドを使って、新しいユーザーをデータベースに追加
        tbl = tables.UserTable.create(
            user_id=profile.sub,
            user_name=self.user_name,
            user_screen_id=profile.preferred_username,
            user_icon_uuid=self.user_icon_uuid,
            user_mail=profile.email,
        )
        tbl.save_new(session)
        await session.commit()
        await session.refresh(tbl)
        return results.UserModel(tbl)


class PostCreatorBody(BaseModel):
    user_id: uuid.UUID
    contact_address: str
    transfer_target: str

    async def save_new(self, user: deps.UserDeps, session: AsyncSession) -> results.CreatorResult:
        creator_table = tables.CreatorTable.create(user.user_table, self.contact_address, self.transfer_target)
        creator_table.save_new(session)
        await session.commit()
        await session.refresh(creator_table)
        return results.CreatorResult(
            creator_table
        )
