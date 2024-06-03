from dataclasses import dataclass
from src.messages.factories import MessageFactory

from .repository import MessagesRepository
from .schemas import Message


@dataclass(kw_only=True)
class MessagesService:
    repository: MessagesRepository

    async def add(self, message: MessageFactory) -> Message:
        new_message_dict = message.model_dump()
        await self.repository.add(new_message_dict)
        return Message(**new_message_dict)

    async def get_many(self, count: int, offset: int) -> list[Message]:
        result = await self.repository.get_many(count, offset)
        return [Message(**message) for message in result]
