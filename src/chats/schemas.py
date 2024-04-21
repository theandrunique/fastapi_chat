from pydantic import BaseModel

from src.schemas import Chat, PrivateChat


class ChatsCollection(BaseModel):
    private_chats: list[PrivateChat]
    group_chats: list[Chat]
