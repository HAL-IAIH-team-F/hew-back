import uuid
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls
from hew_back.chat.__res import ChatRes, ChatMessageRes, MessageRes, ChatMessagesRes

@dataclass
class ChatUsersResult