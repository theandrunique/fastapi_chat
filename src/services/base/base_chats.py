from abc import ABC, abstractmethod
from uuid import UUID
from src.models.chat import Chat
from src.schemas.chats import ChatFactory
from src.schemas.object_id import PyObjectId
from src.models.message import Message


class ChatsService(ABC):
    @abstractmethod
    async def add(self, chat: ChatFactory) -> Chat: ...

    @abstractmethod
    async def get_user_chats(self, user_id: UUID) -> list[Chat]: ...

    @abstractmethod
    async def get(self, chat_id: PyObjectId) -> Chat | None: ...

    @abstractmethod
    async def get_private_chat(
        self, user_1_id: UUID, user_2_id: UUID
    ) -> Chat | None: ...

    async def update_last_message(
        self, chat_id: PyObjectId, new_message: Message
    ) -> None: ...
