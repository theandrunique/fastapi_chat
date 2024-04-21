from pydantic import BaseModel

from src.schemas import ChatType, Message


class MessageCreate(BaseModel):
    text: str


class MessageCollection(BaseModel):
    messages: list[Message]


class PrivateChat(BaseModel):
    id: str
    messages_count: int = 0
    type: ChatType


class PrivateChatsCollection(BaseModel):
    chats: list[PrivateChat]   
