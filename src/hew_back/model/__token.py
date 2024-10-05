from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Union, Optional

from fastapi import Depends
from jose import jwt
from pydantic import BaseModel

from hew_back import error, model
from hew_back.env import ENV
from hew_back.token import oauth2_scheme


class TokenType(str, Enum):
    access = "access"
    refresh = "refresh"


class JwtTokenData(BaseModel):
    exp: datetime
    token_type: TokenType
    profile: model.KeycloakUserProfile

    @staticmethod
    def create(
            exp: datetime, token_type: TokenType, profile: model.KeycloakUserProfile
    ):
        return JwtTokenData(
            exp=exp, token_type=token_type, profile=profile,
        )

    @staticmethod
    def get_token_or_none(token: str | None = Depends(oauth2_scheme))->Optional['JwtTokenData']:
        if token is None:
            return None
        return JwtTokenData(**jwt.decode(token, ENV.token.secret_key, algorithms=[ENV.token.algorithm]))

    @staticmethod
    def get_token(token=Depends(get_token_or_none)):
        token: JwtTokenData | None
        if token is None:
            raise error.ErrorIdException(model.ErrorIds.UNAUTHORIZED)
        return token

    @staticmethod
    def get_access_token_or_none(token=Depends(get_token_or_none))->Optional['JwtTokenData']:
        if token is None:
            return None
        if token.token_type != TokenType.access:
            raise error.ErrorIdException(model.ErrorIds.INVALID_TOKEN)
        return token

    @staticmethod
    def get_refresh_token_or_none(token=Depends(get_token_or_none)):
        if token is None:
            return None
        if token.token_type != TokenType.refresh:
            raise error.ErrorIdException(model.ErrorIds.INVALID_TOKEN)
        return token


class TokenInfo(BaseModel):
    token: str
    expire: datetime

    @staticmethod
    def create_token(token_type: TokenType, res: model.KeycloakUserProfile,
                     expires_delta: timedelta | None = None):
        expire = datetime.now(timezone.utc) + expires_delta
        encoded_jwt = jwt.encode(
            JwtTokenData.create(exp=expire, token_type=token_type, profile=res).model_dump(),
            ENV.token.secret_key,
            algorithm=ENV.token.algorithm
        )
        return TokenInfo(token=encoded_jwt, expire=expire)

    @staticmethod
    def create_refresh_token(res: model.KeycloakUserProfile):
        return TokenInfo.create_token(
            TokenType.refresh, res,
            expires_delta=timedelta(minutes=ENV.token.refresh_token_expire_minutes)
        )

    @staticmethod
    def create_access_token(res: model.KeycloakUserProfile):
        return TokenInfo.create_token(
            TokenType.access, res, timedelta(minutes=ENV.token.access_token_expire_minutes)
        )


class PostTokenBody(BaseModel):
    keycloak_token: str


class TokenRes(BaseModel):
    access: TokenInfo
    refresh: TokenInfo

    @staticmethod
    def create(access: TokenInfo, refresh: TokenInfo):
        return TokenRes(access=access, refresh=refresh)

    @staticmethod
    def create_by_post_token_body(body: PostTokenBody):
        return TokenRes.create_by_keycloak_user_profile_res(
            model.KeycloakUserProfile.create_by_post_token_body(body)
        )

    @staticmethod
    def create_by_jwt_token_data(data: JwtTokenData):
        return TokenRes.create_by_keycloak_user_profile_res(data.profile)

    @staticmethod
    def create_by_keycloak_user_profile_res(profile: model.KeycloakUserProfile):
        return TokenRes.create(
            TokenInfo.create_access_token(profile),
            TokenInfo.create_refresh_token(profile)
        )
