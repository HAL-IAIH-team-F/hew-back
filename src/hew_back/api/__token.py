from urllib.error import HTTPError

from hew_back import app, model
from hew_back.env import ENV
from hew_back.util import urls


@app.post("/api/token")
async def post_token(body: model.PostTokenBody):
    well_knowns = (ENV.keycloak.well_known_url
                   .to_request()
                   .content_type(urls.ContentType.JSON)
                   .add_header("User-Agent", "Application")
                   .fetch()
                   .json_model(model.WellKnownRes)
                   )

    profile = (urls.URL.by_str(well_knowns.userinfo_endpoint)
               .to_request()
               .authorization(urls.BearerAuthorization(body.keycloak_token))
               .add_header("User-Agent", "Application")
               .fetch()
               .on_status_code(401, lambda s: model.ErrorIds.INVALID_TOKEN.value.to_exception().raise_self())
               .json_model(model.KeycloakUserProfileRes)
               )
    return {"ok": True}
