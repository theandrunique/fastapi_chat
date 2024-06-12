from dataclasses import dataclass
from uuid import UUID

from src.models.chat import Chat, ChatType
from src.models.message import Message
from src.repositories.base.base_chats import ChatsRepository
from src.schemas.chats import ChatFactory
from src.schemas.object_id import PyObjectId

from .base.base_chats import ChatsService


@dataclass(kw_only=True)
class ImplChatsService(ChatsService):
    repository: ChatsRepository

    async def add(self, chat: ChatFactory) -> Chat:
        new_chat_dict = chat.model_dump()
        new_chat_id = await self.repository.add(new_chat_dict)
        return Chat(**new_chat_dict, id=new_chat_id)

    async def get_user_chats(self, user_id: UUID) -> list[Chat]:
        chats = await self.repository.get_user_chats(user_id)
        return [Chat(**chat) for chat in chats]

    async def get(self, chat_id: PyObjectId) -> Chat | None:
        result = await self.repository.get(chat_id)
        if result:
            return Chat(**result)
        return None

    async def get_private_chat(self, user_1: UUID, user_2: UUID) -> Chat | None:
        result = await self.repository.get_private_chat(user_1, user_2)
        if result:
            return Chat(**result)
        else:
            chat_factory = ChatFactory(
                type=ChatType.PRIVATE,
                members=[user_1, user_2],
            )
            return await self.add(chat_factory)

    async def update_last_message(
        self, chat_id: PyObjectId, new_message: Message
    ) -> Chat:
        chat_dict = await self.repository.update(
            chat_id,
            {
                "last_message": new_message.model_dump(),
                "message_count": new_message.id + 1,
            },
        )
        return Chat(**chat_dict)
