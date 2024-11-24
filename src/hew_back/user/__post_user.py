import uuid

from fastapi import Depends
from pydantic import field_serializer
from pydantic.dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import deps, tbls, mdls
from hew_back.tbls import UserTable
from hew_back.user.__result import UserResult


@dataclass
class PostUserBody:
    user_name: str
    user_icon_uuid: uuid.UUID | None

    @field_serializer("user_icon_uuid")
    def serialize_sub(self, user_icon_uuid: uuid.UUID) -> str | None:
        if user_icon_uuid is None:
            return None
        return str(user_icon_uuid)


async def __insert_user(
        body: PostUserBody,
        session: AsyncSession = Depends(deps.DbDeps.session),
        token: deps.JwtTokenDeps = Depends(deps.JwtTokenDeps.get_access_token),
) -> UserTable:
    profile = token.profile
    tbl = tbls.UserTable.create(
        user_id=profile.sub,
        user_name=body.user_name,
        user_screen_id=profile.preferred_username,
        user_icon_uuid=body.user_icon_uuid,
        user_mail=profile.email,
    )
    await tbl.save_new(session)
    await session.flush()
    await session.refresh(tbl)
    return tbl


async def __post_images(
        body: PostUserBody,
        img_deps: deps.ImageDeps = Depends(deps.ImageDeps.get),
):
    if body.user_icon_uuid is not None:
        img_deps.crete(mdls.State.public).post_preference(body.user_icon_uuid)


async def post_user(
        _img=Depends(__post_images),
        user=Depends(__insert_user),
) -> UserResult:
    return UserResult(user)
