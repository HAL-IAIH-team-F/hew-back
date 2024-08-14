import abc
from datetime import datetime, timedelta, timezone
from enum import Enum

from fastapi import Depends
from jose import jwt
from pydantic import BaseModel

from hew_back import error, model
from hew_back.env import ENV
from hew_back.token import oauth2_scheme


class TokenType(str, Enum):
    access = "access"
    refresh = "refresh"


class IJwtTokenData(metaclass=abc.ABCMeta):
    pass


class JwtTokenData(BaseModel):
    exp: datetime
    token_type: TokenType
    user_id: int

    @staticmethod
    def create(exp: datetime, token_type: TokenType, user_id: int):
        return JwtTokenData(exp=exp, token_type=token_type, user_id=user_id)

    @staticmethod
    def get_token_or_none(token: str | None = Depends(oauth2_scheme)):
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
    def access_token_or_none(token=Depends(get_token_or_none)):
        if token is None:
            return None
        if token.token_type != "access":
            raise error.ErrorIdException(model.ErrorIds.INVALID_TOKEN)
        return token


class TokenInfo(BaseModel):
    token: str
    expire: datetime

    @staticmethod
    def create_token(user_id: int, token_type: TokenType, expires_delta: timedelta | None = None):
        expire = datetime.now(timezone.utc) + expires_delta
        encoded_jwt = jwt.encode(
            JwtTokenData.create(exp=expire, user_id=user_id, token_type=token_type).model_dump(),
            ENV.token.secret_key,
            algorithm=ENV.token.algorithm
        )
        return TokenInfo(token=encoded_jwt, expire=expire)

    @staticmethod
    def create_refresh_token(user_id: int):
        return TokenInfo.create_token(
            user_id,
            TokenType.refresh,
            expires_delta=timedelta(minutes=ENV.token.refresh_token_expire_minutes)
        )

    @staticmethod
    def create_access_token(user_id: int):
        return TokenInfo.create_token(
            user_id, TokenType.access,
            timedelta(minutes=ENV.token.access_token_expire_minutes)
        )
