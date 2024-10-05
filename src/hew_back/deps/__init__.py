from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel

from hew_back import ENV
from hew_back.util import keycloak, err

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/refresh", auto_error=False)


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
