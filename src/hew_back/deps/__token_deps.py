from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from hew_back import mdls, ENV
from hew_back.util import keycloak, err

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/refresh", auto_error=False)


@dataclass
class JwtTokenDeps:
    jwt_token_data: mdls.JwtTokenData

    @property
    def exp(self) -> datetime:
        return self.jwt_token_data.exp

    @property
    def token_type(self) -> mdls.TokenType:
        return self.jwt_token_data.token_type

    @property
    def profile(self) -> keycloak.KeycloakUserProfile:
        return self.jwt_token_data.profile

    def renew_tokens(self) -> mdls.Tokens:
        return self.jwt_token_data.renew_tokens()

    @staticmethod
    def get_token_or_none(token: str | None = Depends(oauth2_scheme)) -> Optional['JwtTokenDeps']:
        if token is None:
            return None
        return JwtTokenDeps(
            mdls.JwtTokenData(**jwt.decode(token, ENV.token.secret_key, algorithms=[ENV.token.algorithm]))
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
        if token.token_type != token.TokenType.upload:
            raise err.ErrorIdException(err.ErrorIds.INVALID_TOKEN)
        return token

    @staticmethod
    def get_access_token(token=Depends(get_token)) -> 'JwtTokenDeps':
        if token.token_type != mdls.TokenType.access:
            raise err.ErrorIdException(err.ErrorIds.INVALID_TOKEN)
        return token

    @staticmethod
    def get_refresh_token_or_none(token=Depends(get_token_or_none)):
        if token is None:
            return None
        if token.token_type != mdls.TokenType.refresh:
            raise err.ErrorIdException(err.ErrorIds.INVALID_TOKEN)
        return token

    @staticmethod
    def get_refresh_token(token=Depends(get_token)):
        if token.token_type != mdls.TokenType.refresh:
            raise err.ErrorIdException(err.ErrorIds.INVALID_TOKEN)
        return token
