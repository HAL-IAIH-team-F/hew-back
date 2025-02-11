from fastapi import Depends

from hew_back import mdls, deps
from hew_back.util.pydanticutl import Uuid


class UserService:
    def __init__(
            self,
            img_deps: deps.ImageDeps = Depends(deps.ImageDeps.get),
    ):
        self.__img_deps = img_deps

    async def post_images(
            self,
            icon_uuid: Uuid,
    ):
        self.__img_deps.crete(mdls.State.public).post_preference(icon_uuid)
