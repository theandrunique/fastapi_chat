from pydantic import BaseModel

from src.chats.schemas import Chat
from src.messages.schemas import Message


class NewMessage(BaseModel):
    chat: Chat
    message: Message
