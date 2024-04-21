import datetime
from enum import Enum

from pydantic import AliasChoices, BaseModel, Field

from src.mongo.object_id import PyObjectId

class ChatType(str, Enum):
    PRIVATE = "private"
    GROUP = "group"


class Message(BaseModel):
    text: str
    sended_at: datetime.datetime
    from_id: str
    message_id: int


class Chat(BaseModel):
    id: PyObjectId = Field(validation_alias=AliasChoices("id", "_id"), serialization_alias="id")
    name: str | None = None
    messages_count: int
    type: ChatType 
    members: list[str]


class PrivateChat(BaseModel):
    id: PyObjectId = Field(validation_alias=AliasChoices("id", "_id"), serialization_alias="id")
    name: str | None = None
    messages_count: int = 0
    type: ChatType


class UserChat(BaseModel):
    chat_id: str
    type: ChatType
