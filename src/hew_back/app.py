import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# from icha.env import cors_list
# from icha.util.logger_filter import ExcludeFilter

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel("INFO")

app = FastAPI()

# logging.getLogger("uvicorn.access").addFilter(ExcludeFilter(["/health"]))

# if cors_list is None:
#     cors_list = "*"
app.add_middleware(
    CORSMiddleware,
    # allow_origins=cors_list.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 14

# noinspection PyUnresolvedReferences
# import icha.apis
# noinspection PyUnresolvedReferences
# import icha.error

# from icha.cmd import job

# app.cli.add_command(job)
