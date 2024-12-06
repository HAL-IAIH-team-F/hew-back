import pydantic.dataclasses
from pydantic import BaseModel

from hew_back import mdls
from hew_back.util import tks
from hew_back.util.tks import TokenInfo


class TokenResOld(BaseModel):
    access: tks.TokenInfoOld
    refresh: tks.TokenInfoOld

    @staticmethod
    def from_tokens(tokens: mdls.Tokens):
        return TokenResOld.create(tokens.access, tokens.refresh)

    @staticmethod
    def create(access: tks.TokenInfoOld, refresh: tks.TokenInfoOld):
        return TokenResOld(access=access, refresh=refresh)


@pydantic.dataclasses.dataclass
class TokenRes:
    access: tks.TokenInfo
    refresh: tks.TokenInfo

    @staticmethod
    def from_tokens(tokens: mdls.Tokens):
        return TokenRes(
            TokenInfo(tokens.access.token, tokens.access.expire),
            TokenInfo(tokens.refresh.token, tokens.refresh.expire),
        )


class ImgTokenRes(BaseModel):
    upload: tks.TokenInfoOld

    @staticmethod
    def from_img_tokens(tokens: mdls.ImgTokens):
        return ImgTokenRes.create(tokens.upload)

    @staticmethod
    def create(upload: tks.TokenInfoOld):
        return ImgTokenRes(upload=upload)
