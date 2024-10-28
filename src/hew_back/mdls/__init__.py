import uuid
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from enum import Enum
from uuid import UUID

from pydantic import field_serializer, BaseModel

from hew_back import ENV
from hew_back.util import tks, keycloak, urls
from hew_back.util.err import ErrorIds


@dataclass
class Tokens:
    access: tks.TokenInfo
    refresh: tks.TokenInfo


@dataclass

class ImgTokens:
    upload: tks.TokenInfo


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


class ImgTokenType(tks.AbcTokenType, Enum):
    upload = "Upload"


class ImgJwtTokenData(tks.AbcJwtTokenData[ImgTokenType]):
    uuid: UUID

    def new_img_tokens(self) -> ImgTokens:
        return ImgTokens(
            self.new_token_info(ENV.token.img_secret_key)
        )

    @field_serializer("uuid")
    def serialize_sub(self, uid: UUID) -> str:
        return str(uid)

    @staticmethod
    def new(
            token_type: ImgTokenType, img_uuid: UUID
    ) -> 'ImgJwtTokenData':
        if token_type == ImgTokenType.upload:
            exp = datetime.now(timezone.utc) + timedelta(ENV.token.access_token_expire_minutes)
        else:
            raise ValueError(f"Unknown token type: {token_type}")
        return ImgJwtTokenData(
            exp=exp, token_type=token_type, uuid=img_uuid,
        )


class State(str, Enum):
    public = "Public"
    private = "Private"


class ImagePreferenceRequest(BaseModel):
    state: State

    @staticmethod
    def crete(state: State) -> 'ImagePreferenceRequest':
        return ImagePreferenceRequest(state=state)

    def post_preference(self, img_uuid: uuid.UUID):
        (ENV.img_url.join_path(f"/preference/{img_uuid}")
         .to_request()
         .set_method(urls.HttpMethod.PUT)
         .body(self.model_dump_json().encode())
         .content_type(urls.ContentType.JSON)
         .fetch()
         .on_status_code(404, lambda s: ErrorIds.CONTENT_IMAGE_NOT_FOUND.to_exception("img id not found").raise_self())
         .on(lambda s: s.status_code != 200,
             lambda s: ErrorIds.INTERNAL_API_ERROR.to_exception(f"{s.status_code}: {s.body()}").raise_self())
         .body()
         )


class Img(BaseModel):
    image_uuid: uuid.UUID
    token: str | None

    @staticmethod
    def create(img_uuid: uuid.UUID, token: str | None) -> 'Img':
        return Img(
            image_uuid=img_uuid,
            token=token,
        )
