from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from hew_back.util import keycloak


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
