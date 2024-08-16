from http import client
from http.client import HTTPResponse
from typing import Final

from pydantic import BaseModel

from . import HttpRequest


####################################################################################################
# httpレスポンスに関するもの
class HttpResponse:
    """httpレスポンスを表すクラス
    """
    http_request: Final[HttpRequest]
    response: Final[HTTPResponse]

    def json_model[T: BaseModel](self, model: type[T]):
        """responseのbodyをjsonオブジェクトに変換する
        :return: jsonを表すディクショナリ
        """
        return model.model_validate_json(self.body())

    def body(self):
        encoding = self.response.headers.get_content_charset('utf-8')
        return self.response.read().decode(encoding)

    def status_code(self):
        """http status codeを取得します
        :return: status codeの数字
        """
        return self.response.getcode()

    def __init__(self, http_request: HttpRequest, response: client.HTTPResponse):
        self.http_request = http_request
        self.response = response

    def __enter__(self):
        self.response.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.response.__exit__(exc_type, exc_val, exc_tb)
