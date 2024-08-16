from typing import Self
from urllib import parse


####################################################################################################
# urlに関するもの

class URL:
    """urlを扱うためのクラス
    :var __parse_result: urlの情報
    """
    __parse_result: parse.ParseResult

    def __init__(self, parse_result: parse.ParseResult):
        self.__parse_result = parse_result

    @staticmethod
    def by_str(url: str):
        """文字列のurlからURLオブジェクトを作成します
        :param url: 文字列のurl
        """
        result = parse.urlparse(url)
        return URL(result)

    def join_path(self, path: str) -> Self:
        """既存のurlにpathを追加します
        :param path: 追加するpath
        """
        path = parse.urljoin(self.__parse_result.path, path)
        self.__parse_result = self.__parse_result._replace(path=path)
        return self

    def join_query(self, query: dict[str, str]) -> Self:
        """join query parm
        """
        exit_query = parse.parse_qs(self.__parse_result.query)
        str_query = parse.urlencode({**exit_query, **query})
        self.__parse_result = self.__parse_result._replace(query=str_query)
        return self

    def to_str_url(self):
        return parse.urlunparse(self.__parse_result)

    def __str__(self):
        return self.__parse_result.__str__()

    def to_request(self):
        from . import HttpRequest
        return HttpRequest.by_url(self)
