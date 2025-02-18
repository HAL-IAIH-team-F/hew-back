from datetime import datetime

from fastapi import Depends
from jose import jwt, ExpiredSignatureError

from hew_back import mdls, ENV
from hew_back.deps import oauth2_scheme
from hew_back.util import err
from hew_back.util.err import ErrorIds
from hew_back.util.pydanticutl import Uuid
from hew_back.util.tks import TokenInfo


class FileAccessTokenDeps:
    jwt_token_data: mdls.FileAccessJwtTokenData | None

    @property
    def exp(self) -> datetime:
        return self.jwt_token_data.exp

    @property
    def token_type(self) -> mdls.FileTokenType:
        return self.jwt_token_data.token_type

    @property
    def file_uuid(self) -> Uuid:
        return self.jwt_token_data.file_uuid

    def renew_tokens(self) -> TokenInfo:
        return self.jwt_token_data.new_token_info(ENV.token.img_secret_key)

    def __init__(self, token: str | None = Depends(oauth2_scheme)):
        if token is None:
            self.jwt_token_data = None
            return
        try:
            result = jwt.decode(token, ENV.token.secret_key, algorithms=[ENV.token.algorithm])
        except ExpiredSignatureError:
            raise ErrorIds.TOKEN_EXPIRED.to_exception()
        self.jwt_token_data = mdls.FileAccessJwtTokenData(**result)
        if self.jwt_token_data.token_type != mdls.FileTokenType.access:
            raise err.ErrorIdException(err.ErrorIds.INVALID_TOKEN)
