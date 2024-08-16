from abc import ABC
from enum import Enum
from typing import Self
from urllib import request

from . import URL


####################################################################################################
class ContentType(Enum):
    JSON = "application/json"
    GITHUB_JSON = "application/vnd.github+json"


class AuthorizationValue(
    ABC
):
    def __init__(self, value: str):
        self.value = value


class BearerAuthorization(AuthorizationValue):
    def __init__(self, token: str):
        super().__init__(f"Bearer {token}")


# httpリクエストに関するもの
class HttpRequest:
    """httpリクエストの情報を扱うクラス
    :var _url_request: リクエストの情報
    """
    _url_request: request.Request

    def __init__(self, url_request: request.Request):
        self._url_request = url_request

    @staticmethod
    def by_url(url: URL):
        """指定されたurlからHttpRequestを作成します
        """
        return HttpRequest(request.Request(url.to_str_url()))

    def get_request(self) -> request.Request:
        """現在のリクエストを取得します
        """
        return self._url_request

    def accept(self, content_type: ContentType) -> Self:
        self.add_header("Accept", content_type.value)
        return self

    def authorization(self, value: AuthorizationValue) -> Self:
        self.add_header("Authorization", value.value)
        return self

    def add_header(self, header: str, value: str) -> Self:
        self._url_request.add_header(header, value)
        return self

    def set_method(self, method: str) -> Self:
        self._url_request.method = method
        return self

    def fetch(self):
        from kutilpy.kutil.urls.http_client import HttpClient
        return HttpClient.fetch(self)

    def __str__(self):
        return f"HttpRequest: '{self._url_request.method} {self._url_request.full_url}'"
