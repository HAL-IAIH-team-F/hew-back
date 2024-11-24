import uuid

from pydantic import BaseModel, field_serializer
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import  mdls, tbls
from hew_back.user.__result import UserResult
from hew_back.util import keycloak

