import uuid
# noinspection PyUnresolvedReferences
from dataclasses import dataclass
from typing import Annotated
from uuid import UUID

from pydantic import field_serializer, BaseModel, AfterValidator, PlainSerializer

from .__token import *


@dataclass
class ImgTokens:
    upload: tks.TokenInfoOld


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


class Img(BaseModel):
    image_uuid: uuid.UUID
    token: str | None

    @staticmethod
    def create(img_uuid: uuid.UUID, token: str | None) -> 'Img':
        return Img(
            image_uuid=img_uuid,
            token=token,
        )

