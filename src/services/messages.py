from dataclasses import dataclass

from src.repositories.base.base_messages import MessagesRepository
from src.schemas.messages import MessageFactory
from src.models.message import Message

from .base.base_messages import MessagesService


@dataclass(kw_only=True)
class ImplMessagesService(MessagesService):
    repository: MessagesRepository

    async def add(self, message: MessageFactory) -> Message:
        new_message_dict = message.model_dump()
        await self.repository.add(new_message_dict)
        return Message(**new_message_dict)

    async def get_many(self, count: int, offset: int) -> list[Message]:
        result = await self.repository.get_many(count, offset)
        return [Message(**message) for message in result]
