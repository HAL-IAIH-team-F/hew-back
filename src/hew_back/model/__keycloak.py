from pydantic import BaseModel


class WellKnownRes(BaseModel):
    userinfo_endpoint: str
# {"sub":"b38dc1a6-73c1-46aa-adeb-a969fd89c09f","email_verified":false,"preferred_username":"kigawa","email":"account@kigawa.net"}
class KeycloakUserProfileRes(BaseModel):
    sub: str
    email_verified: bool
    preferred_username: str
    email: str