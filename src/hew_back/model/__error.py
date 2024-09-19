from enum import Enum

from pydantic import BaseModel


class ErrorId(BaseModel):
    message: str
    status_code: int

    @staticmethod
    def create(message: str, status_code: int):
        return ErrorId(message=message, status_code=status_code)

    def to_exception(self, message: str | None = None):
        from hew_back import error
        return error.ErrorIdException(self, message)


class ErrorIds(Enum):
    INTERNAL_ERROR = ErrorId.create("server internal error", 500)
    GET_PROFILE_FAILED = ErrorId.create("get profile failed", 500)

    PASSWORD_EMPTY = ErrorId.create("password is empty", 400)
    USER_NOT_FOUND = ErrorId.create("user not found", 404)

    UNAUTHORIZED = ErrorId.create("unauthorized", 401)
    UNAUTHORIZED_TOKEN = ErrorId.create("unauthorized token", 401)
    NOT_PERMITTED = ErrorId.create("not permitted", 401)

    NOT_FOUND = ErrorId.create("404 not found", 404)
    GACHA_NOT_FOUND = ErrorId.create("gacha not found", 404)
    GACHA_CONTENT_NOT_FOUND = ErrorId.create("gacha content not found", 404)
    CONTENT_IMAGE_NOT_FOUND = ErrorId.create("content image not found", 404)
    THUMBNAIL_NOT_FOUND = ErrorId.create("thumbnail not found", 404)

    USER_NAME_CONFLICT = ErrorId.create("user name conflict", 409)
    TOKEN_CONFLICT = ErrorId.create("token conflict", 409)
    TOKEN_EXPIRED = ErrorId.create("token expired", 409)
    INVALID_TOKEN = ErrorId.create("token invalid", 409)
    USER_LOGIN_FAILED = ErrorId.create("user login failed, invalid name or password", 409)
    ALL_GACHA_PULLED = ErrorId.create("all gacha were pulled", 409)


class ErrorRes(BaseModel):
    error_id: str
    message: str

    @staticmethod
    def create(error_id: str, message: str):
        return ErrorRes(error_id=error_id, message=message)

    @staticmethod
    def create_by_exception(e: Exception, error_ids: ErrorIds = ErrorIds.INTERNAL_ERROR):
        return ErrorRes.create(
            error_id=error_ids.name,
            message=e.__str__()
        )
