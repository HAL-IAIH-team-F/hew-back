import uvicorn

import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel("INFO")

app = FastAPI()


# logging.getLogger("uvicorn.access").addFilter(ExcludeFilter(["/health"]))

# if cors_list is None:
#     cors_list = "*"


class Main:
    def __init__(self, fast_api: FastAPI):
        self.app = fast_api
        fast_api.add_middleware(
            CORSMiddleware,
            # allow_origins=cors_list.split(","),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 15
        self.REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 14

        # noinspection PyUnresolvedReferences
        import hew_back.api

    def main(self):
        uvicorn.run(self.app, host="0.0.0.0")


main = Main(app)
