from pydantic import BaseModel

from hew_back import ENV, mdls
from hew_back.util import keycloak


class PostTokenBody(BaseModel):
    keycloak_token: str

    def fetch_keycloak_profile(self) -> keycloak.KeycloakUserProfile:
        well_known = keycloak.WellKnown.fetch(ENV.keycloak.well_known_url)
        return keycloak.KeycloakUserProfile.fetch(well_known, self.keycloak_token)

    def new_tokens(self):
        profile = self.fetch_keycloak_profile()
        print(profile)
        return mdls.Tokens(
            access=mdls.JwtTokenData.new(
                mdls.TokenType.access,
                profile
            ).new_token_info(ENV.token.secret_key),
            refresh=mdls.JwtTokenData.new(
                mdls.TokenType.refresh,
                profile
            ).new_token_info(ENV.token.secret_key)
        )
