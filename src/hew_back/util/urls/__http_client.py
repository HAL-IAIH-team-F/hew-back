from urllib import request

from . import HttpResponse
from . import HttpRequest


####################################################################################################
# httpアクセスに関するもの
class HttpClient:
    """httpを使用したアクセスを行います
    """

    @staticmethod
    def fetch(http_request: HttpRequest) -> HttpResponse:
        """requestを使用してhttpアクセスを行います
        :param http_request: アクセスに使用する情報
        :return: リクエストの結果 with構文を使用する必要があります
        """
        return HttpResponse(http_request, request.urlopen(http_request.get_request()))
