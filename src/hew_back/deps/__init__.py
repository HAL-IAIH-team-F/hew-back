from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import ENV, tables, responses, models
from hew_back.db import DB
from hew_back.models import TokenType
from hew_back.util import err, keycloak

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/refresh", auto_error=False)


class DbDeps:
    @staticmethod
    async def session() -> AsyncSession:
        async with DB.session_maker() as session:
            yield session


@dataclass
class JwtTokenDeps:
    jwt_token_data: models.JwtTokenData

    @property
    def exp(self) -> datetime:
        return self.jwt_token_data.exp

    @property
    def token_type(self) -> TokenType:
        return self.jwt_token_data.token_type

    @property
    def profile(self) -> keycloak.KeycloakUserProfile:
        return self.jwt_token_data.profile

    def to_token_res(self) -> responses.TokenRes:
        return responses.TokenRes.create_by_keycloak_user_profile(self.profile)

    @staticmethod
    def get_token_or_none(token: str | None = Depends(oauth2_scheme)) -> Optional['JwtTokenDeps']:
        if token is None:
            return None
        return JwtTokenDeps(
            models.JwtTokenData(**jwt.decode(token, ENV.token.secret_key, algorithms=[ENV.token.algorithm]))
        )

    @staticmethod
    def get_token(token=Depends(get_token_or_none)):
        token: JwtTokenDeps | None
        if token is None:
            raise err.ErrorIdException(err.ErrorIds.UNAUTHORIZED)
        return token

    @staticmethod
    def get_access_token_or_none(token=Depends(get_token_or_none)) -> Optional['JwtTokenDeps']:
        if token is None:
            return None
        if token.token_type != models.TokenType.access:
            raise err.ErrorIdException(err.ErrorIds.INVALID_TOKEN)
        return token

    @staticmethod
    def get_refresh_token_or_none(token=Depends(get_token_or_none)):
        if token is None:
            return None
        if token.token_type != models.TokenType.refresh:
            raise err.ErrorIdException(err.ErrorIds.INVALID_TOKEN)
        return token


@dataclass
class UserDeps:
    user_table: tables.UserTable

    def to_self_user_res(self) -> responses.SelfUserRes:
        return responses.SelfUserRes.create_by_user_table(self.user_table)

    @staticmethod
    async def get_or_none(
            session: AsyncSession = Depends(DbDeps.session),
            token: JwtTokenDeps = Depends(JwtTokenDeps.get_access_token_or_none),
    ) -> Union['UserDeps', None]:
        table = await tables.UserTable.find_one_or_none(session, token.profile.sub)
        if table is None:
            return None
        table.user_mail = token.profile.email
        table.user_screen_id = token.profile.preferred_username
        await session.commit()
        await session.refresh(table)
        return UserDeps(table)

    @staticmethod
    async def get(
            session: AsyncSession = Depends(DbDeps.session),
            token: JwtTokenDeps = Depends(JwtTokenDeps.get_access_token_or_none),
    ) -> 'UserDeps':
        table = await tables.UserTable.find_one(session, token.profile.sub)
        table.user_mail = token.profile.email
        table.user_screen_id = token.profile.preferred_username
        await session.commit()
        await session.refresh(table)
        return UserDeps(table)
