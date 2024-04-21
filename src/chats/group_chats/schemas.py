from pydantic import BaseModel

from src.schemas import ChatType


class ChatCreate(BaseModel):
    name: str


class ChatCreateDefaultValues(ChatCreate):
    name: str
    messages_count: int = 0
    type: ChatType = ChatType.GROUP
