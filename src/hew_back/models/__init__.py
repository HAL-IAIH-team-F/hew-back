from dataclasses import dataclass
from datetime import datetime

from hew_back import responses
from hew_back.util import tokens, keycloak


@dataclass
class Tokens:
    access: tokens.TokenInfo
    refresh: tokens.TokenInfo

    def to_token_res(self):
        return responses.TokenRes.create(
            self.access,
            self.refresh,
        )


class JwtTokenData(tokens.AbcJwtTokenData):
    profile: keycloak.KeycloakUserProfile

    @staticmethod
    def create(
            exp: datetime, token_type: tokens.TokenType, profile: keycloak.KeycloakUserProfile
    ):
        return JwtTokenData(
            exp=exp, token_type=token_type, profile=profile,
        )
