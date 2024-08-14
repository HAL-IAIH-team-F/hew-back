from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/refresh", auto_error=False)

# async def get_login_user_or_none(
#         session: AsyncSession = Depends(get_session),
#         token: data.JwtTokenData | None = Depends(access_token_or_none)
# ):
#     if token is None:
#         return None
#     user = await user_repo.by_token(session, token)
#     await session.refresh(user)
#     return user
#
#
# async def get_login_user(
#         user: UserTable | None = Depends(get_login_user_or_none)
# ) -> UserTable:
#     if user is None:
#         raise ErrorIdException(ErrorIds.UNAUTHORIZED)
#     return user
