from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from enum import Enum
from uuid import UUID

from hew_back import responses, ENV
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


@dataclass
class ImgTokens:
    upload: tokens.TokenInfo

    def to_img_token_res(self) -> responses.ImgTokenRes:
        return responses.ImgTokenRes.create(
            self.upload,
        )


class TokenType(tokens.AbcTokenType, Enum):
    access = "access"
    refresh = "refresh"


class JwtTokenData(tokens.AbcJwtTokenData[TokenType]):
    profile: keycloak.KeycloakUserProfile

    def renew_tokens(self):
        return Tokens(
            JwtTokenData.new(TokenType.access, self.profile).new_token_info(),
            JwtTokenData.new(TokenType.refresh, self.profile).new_token_info(),
        )

    @staticmethod
    def new(
            token_type: TokenType, profile: keycloak.KeycloakUserProfile
    ):
        if token_type == TokenType.access:
            exp = datetime.now(timezone.utc) + timedelta(ENV.token.access_token_expire_minutes)
        elif token_type == TokenType.refresh:
            exp = datetime.now(timezone.utc) + timedelta(ENV.token.refresh_token_expire_minutes)
        else:
            raise ValueError(f"Unknown token type: {token_type}")
        return JwtTokenData(
            exp=exp, token_type=token_type, profile=profile,
        )


class ImgTokenType(tokens.AbcTokenType, Enum):
    upload = "Upload"


class ImgJwtTokenData(tokens.AbcJwtTokenData[ImgTokenType]):
    uuid: UUID

    def new_img_tokens(self) -> ImgTokens:
        return ImgTokens(
            self.new_token_info()
        )

    @staticmethod
    def new(
            token_type: ImgTokenType, uuid: UUID
    ) -> 'ImgJwtTokenData':
        if token_type == ImgTokenType.upload:
            exp = datetime.now(timezone.utc) + timedelta(ENV.token.access_token_expire_minutes)
        else:
            raise ValueError(f"Unknown token type: {token_type}")
        return ImgJwtTokenData(
            exp=exp, token_type=token_type, uuid=uuid,
        )
