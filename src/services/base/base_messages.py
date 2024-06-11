from abc import ABC, abstractmethod
from src.models.message import Message
from src.schemas.messages import MessageFactory


class MessagesService(ABC):
    @abstractmethod
    async def add(self, message: MessageFactory) -> Message: ...

    @abstractmethod
    async def get_many(self, count: int, offset: int) -> list[Message]: ...
