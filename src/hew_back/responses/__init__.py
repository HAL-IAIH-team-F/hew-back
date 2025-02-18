from pydantic import BaseModel

from pydantic import BaseModel

from hew_back import mdls
from hew_back.util import tks


class TokenRes(BaseModel):
    access: tks.TokenInfo
    refresh: tks.TokenInfo

    @staticmethod
    def from_tokens(tokens: mdls.Tokens):
        return TokenRes.create(tokens.access, tokens.refresh)

    @staticmethod
    def create(access: tks.TokenInfo, refresh: tks.TokenInfo):
        return TokenRes(access=access, refresh=refresh)


class ImgTokenRes(BaseModel):
    upload: tks.TokenInfo

    @staticmethod
    def from_img_tokens(tokens: mdls.ImgTokens):
        return ImgTokenRes.create(tokens.upload)

    @staticmethod
    def create(upload: tks.TokenInfo):
        return ImgTokenRes(upload=upload)
