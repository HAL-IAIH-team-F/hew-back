import abc
from datetime import datetime
from enum import Enum

from jose import jwt
from pydantic import BaseModel

from .. import ENV


class AbcTokenType(str, Enum):
    pass


class AbcJwtTokenData[T: AbcTokenType](BaseModel, metaclass=abc.ABCMeta):
    exp: datetime
    token_type: T

    def new_token_info(self) -> 'TokenInfo':
        encoded_jwt = jwt.encode(
            self.model_dump(),
            ENV.token.secret_key,
            algorithm=ENV.token.algorithm
        )
        return TokenInfo.create(encoded_jwt, self.exp)


class TokenInfo(BaseModel):
    token: str
    expire: datetime

    @staticmethod
    def create(
            token: str,
            expire: datetime,
    ):
        return TokenInfo(token=token, expire=expire)
