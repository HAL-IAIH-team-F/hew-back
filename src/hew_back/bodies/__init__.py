import uuid

from pydantic import BaseModel, field_serializer
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import ENV, tables, results, deps, mdls
from hew_back.util import keycloak


class PostTokenBody(BaseModel):
    keycloak_token: str

    def fetch_keycloak_profile(self) -> keycloak.KeycloakUserProfile:
        well_known = keycloak.WellKnown.fetch(ENV.keycloak.well_known_url)
        return keycloak.KeycloakUserProfile.fetch(well_known, self.keycloak_token)

    def new_tokens(self):
        profile = self.fetch_keycloak_profile()
        return mdls.Tokens(
            access=mdls.JwtTokenData.new(
                mdls.TokenType.access,
                profile
            ).new_token_info(ENV.token.secret_key),
            refresh=mdls.JwtTokenData.new(
                mdls.TokenType.refresh,
                profile
            ).new_token_info(ENV.token.secret_key)
        )


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
    ) -> results.UserModel:
        if self.user_icon_uuid is not None:
            mdls.ImagePreferenceRequest.crete(mdls.State.public).post_preference(self.user_icon_uuid)

        tbl = tables.UserTable.create(
            user_id=profile.sub,
            user_name=self.user_name,
            user_screen_id=profile.preferred_username,
            user_icon_uuid=self.user_icon_uuid,
            user_mail=profile.email,
        )
        await tbl.save_new(session)
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
