import uuid

from pydantic import RootModel
from pydantic.dataclasses import dataclass

from hew_back import mdls, ENV
from hew_back.util import urls
from hew_back.util.err import ErrorIds


@dataclass
class ImageDeps:
    @staticmethod
    def get():
        return ImageDeps()

    def crete(self, state: mdls.State) -> 'ImagePreferenceRequest':
        return self.ImagePreferenceRequest(state=state)

    @dataclass
    class ImagePreferenceRequest:
        state: mdls.State

        def post_preference(self, img_uuid: uuid.UUID):
            (ENV.img_url.join_path(f"/preference/{img_uuid}")
             .to_request()
             .set_method(urls.HttpMethod.PUT)
             .body(RootModel(self).encode())
             .content_type(urls.ContentType.JSON)
             .fetch()
             .on_status_code(404,
                             lambda s: ErrorIds.CONTENT_IMAGE_NOT_FOUND.to_exception("img id not found").raise_self())
             .on(lambda s: s.status_code != 200,
                 lambda s: ErrorIds.INTERNAL_API_ERROR.to_exception(f"{s.status_code}: {s.body()}").raise_self())
             .body()
             )
