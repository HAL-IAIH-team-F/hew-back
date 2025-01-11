import abc
from datetime import datetime
from enum import Enum

import pydantic.dataclasses
from jose import jwt
from pydantic import RootModel, BaseModel

from . import pydanticutl
from .. import ENV


class AbcTokenType(str, Enum):
    pass


class AbcJwtTokenData[T: AbcTokenType](BaseModel, metaclass=abc.ABCMeta):
    exp: datetime
    token_type: T

    def new_token_info(self, secret: str) -> 'TokenInfo':
        encoded_jwt = jwt.encode(
            RootModel(self).model_dump(),
            secret,
            algorithm=ENV.token.algorithm
        )
        return TokenInfo(encoded_jwt, self.exp)


@pydantic.dataclasses.dataclass
class TokenInfoOld:
    token: str
    expire: datetime


@pydantic.dataclasses.dataclass
class TokenInfo:
    token: str
    expire: pydanticutl.Datetime
