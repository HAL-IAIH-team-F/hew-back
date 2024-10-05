from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional

from fastapi import Depends
from jose import jwt
from pydantic import BaseModel

from hew_back.deps import oauth2_scheme
from hew_back.env import ENV
from hew_back.util import err, keycloak


class TokenType(str, Enum):
    access = "access"
    refresh = "refresh"


class JwtTokenData(BaseModel):
    exp: datetime
    token_type: TokenType
    profile: keycloak.KeycloakUserProfile

    @staticmethod
    def create(
            exp: datetime, token_type: TokenType, profile: keycloak.KeycloakUserProfile
    ):
        return JwtTokenData(
            exp=exp, token_type=token_type, profile=profile,
        )

    @staticmethod
    def get_token_or_none(token: str | None = Depends(oauth2_scheme)) -> Optional['JwtTokenData']:
        if token is None:
            return None
        return JwtTokenData(**jwt.decode(token, ENV.token.secret_key, algorithms=[ENV.token.algorithm]))

    @staticmethod
    def get_token(token=Depends(get_token_or_none)):
        token: JwtTokenData | None
        if token is None:
            raise err.ErrorIdException(err.ErrorIds.UNAUTHORIZED)
        return token

    @staticmethod
    def get_access_token_or_none(token=Depends(get_token_or_none)) -> Optional['JwtTokenData']:
        if token is None:
            return None
        if token.token_type != TokenType.access:
            raise err.ErrorIdException(err.ErrorIds.INVALID_TOKEN)
        return token

    @staticmethod
    def get_refresh_token_or_none(token=Depends(get_token_or_none)):
        if token is None:
            return None
        if token.token_type != TokenType.refresh:
            raise err.ErrorIdException(err.ErrorIds.INVALID_TOKEN)
        return token


class TokenInfo(BaseModel):
    token: str
    expire: datetime

    @staticmethod
    def create_token(token_type: TokenType, res: keycloak.KeycloakUserProfile,
                     expires_delta: timedelta | None = None):
        expire = datetime.now(timezone.utc) + expires_delta
        encoded_jwt = jwt.encode(
            JwtTokenData.create(exp=expire, token_type=token_type, profile=res).model_dump(),
            ENV.token.secret_key,
            algorithm=ENV.token.algorithm
        )
        return TokenInfo(token=encoded_jwt, expire=expire)

    @staticmethod
    def create_refresh_token(res: keycloak.KeycloakUserProfile):
        return TokenInfo.create_token(
            TokenType.refresh, res,
            expires_delta=timedelta(minutes=ENV.token.refresh_token_expire_minutes)
        )

    @staticmethod
    def create_access_token(res: keycloak.KeycloakUserProfile):
        return TokenInfo.create_token(
            TokenType.access, res, timedelta(minutes=ENV.token.access_token_expire_minutes)
        )

