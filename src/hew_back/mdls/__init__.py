import uuid
# noinspection PyUnresolvedReferences
from dataclasses import dataclass
from uuid import UUID

from pydantic import field_serializer, BaseModel

from .__token import *
from ..util import pydanticutl


@dataclass
class ImgTokens:
    upload: tks.TokenInfoOld


class ImgTokenType(tks.AbcTokenType, Enum):
    upload = "Upload"
    access = "Access"


class ImgJwtTokenData(tks.AbcJwtTokenData[ImgTokenType]):
    file_uuid: UUID

    def new_img_tokens(self) -> ImgTokens:
        return ImgTokens(
            self.new_token_info(ENV.token.img_secret_key)
        )

    @field_serializer("file_uuid")
    def serialize_sub(self, uid: UUID) -> str:
        return str(uid)

    @staticmethod
    def new(
            token_type: ImgTokenType, file_uuid: UUID
    ) -> 'ImgJwtTokenData':
        if token_type == ImgTokenType.upload:
            exp = datetime.now(timezone.utc) + timedelta(ENV.token.access_token_expire_minutes)
        else:
            raise ValueError(f"Unknown token type: {token_type}")
        return ImgJwtTokenData(
            exp=exp, token_type=token_type, file_uuid=file_uuid,
        )


class FileAccessJwtTokenData(tks.AbcJwtTokenData[ImgTokenType]):
    file_uuid: pydanticutl.Uuid

    def new_img_tokens(self) -> tks.TokenInfo:
        return self.new_token_info(ENV.token.img_secret_key)

    @field_serializer("file_uuid")
    def serialize_sub(self, uid: UUID) -> str:
        return str(uid)

    @staticmethod
    def new(
            token_type: ImgTokenType, file_uuid: UUID
    ) -> 'FileAccessJwtTokenData':
        exp = datetime.now(timezone.utc) + timedelta(ENV.token.access_token_expire_minutes)
        return FileAccessJwtTokenData(
            exp=exp, token_type=TokenType.access, file_uuid=file_uuid,
        )


class State(str, Enum):
    public = "Public"
    private = "Private"


class Img(BaseModel):
    image_uuid: uuid.UUID
    token: str | None

    @staticmethod
    def create(img_uuid: uuid.UUID, token: str | None) -> 'Img':
        return Img(
            image_uuid=img_uuid,
            token=token,
        )
