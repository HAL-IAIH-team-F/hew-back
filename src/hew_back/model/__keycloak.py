from pydantic import BaseModel

from hew_back import model
from hew_back.env import ENV
from hew_back.util import urls


class WellKnownRes(BaseModel):
    userinfo_endpoint: str

    @staticmethod
    def create():
        return (ENV.keycloak.well_known_url
                .to_request()
                .content_type(urls.ContentType.JSON)
                .add_header("User-Agent", "Application")
                .fetch()
                .json_model(model.WellKnownRes)
                )


class KeycloakUserProfile(BaseModel):
    sub: str
    email_verified: bool
    preferred_username: str
    email: str

    @staticmethod
    def create_by_post_token_body(body):
        """
        create KeycloakUserProfileRes by PostTokenBody
        :param body: model.PostTokenBody
        """
        well_knowns = model.WellKnownRes

        return (urls.URL.by_str(well_knowns.userinfo_endpoint)
                .to_request()
                .authorization(urls.BearerAuthorization(body.keycloak_token))
                .add_header("User-Agent", "Application")
                .fetch()
                .on_status_code(401, lambda s: model.ErrorIds.INVALID_TOKEN.value.to_exception().raise_self())
                .json_model(model.KeycloakUserProfile)
                )
