from datetime import datetime
from uuid import UUID
from enum import Enum


from pydantic import BaseModel, Field, AliasChoices

from src.models.message import Message
from src.schemas.object_id import PyObjectId


class ChatType(str, Enum):
    PRIVATE = "private"
    GROUP = "group"


class Chat(BaseModel):
    id: UUID | PyObjectId = Field(validation_alias=AliasChoices("_id", "id"))
    name: str | None = None
    created_at: datetime
    creator_id: UUID | None = None
    members: list[UUID]
    admins: list[UUID]
    image_url: str | None = None
    message_count: int
    last_message: Message | None = None
    type: ChatType
