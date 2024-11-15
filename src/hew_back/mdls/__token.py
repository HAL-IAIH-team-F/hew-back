from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from enum import Enum

from hew_back import ENV
from hew_back.util import tks, keycloak


@dataclass
class Tokens:
    access: tks.TokenInfo
    refresh: tks.TokenInfo


class TokenType(tks.AbcTokenType, Enum):
    access = "access"
    refresh = "refresh"


class JwtTokenData(tks.AbcJwtTokenData[TokenType]):
    profile: keycloak.KeycloakUserProfile

    def renew_tks(self):
        return Tokens(
            JwtTokenData.new(TokenType.access, self.profile).new_token_info(ENV.token.secret_key),
            JwtTokenData.new(TokenType.refresh, self.profile).new_token_info(ENV.token.secret_key),
        )

    @staticmethod
    def new(
            token_type: TokenType, profile: keycloak.KeycloakUserProfile
    ) -> 'JwtTokenData':
        if token_type == TokenType.access:
            exp = datetime.now(timezone.utc) + timedelta(ENV.token.access_token_expire_minutes)
        elif token_type == TokenType.refresh:
            exp = datetime.now(timezone.utc) + timedelta(ENV.token.refresh_token_expire_minutes)
        else:
            raise ValueError(f"Unknown token type: {token_type}")
        return JwtTokenData(
            exp=exp, token_type=token_type, profile=profile,
        )
