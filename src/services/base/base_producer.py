from abc import ABC, abstractmethod
from uuid import UUID

from src.schemas.messages import NewMessage


class ProducerService(ABC):
    @abstractmethod
    async def send_message(self, message: NewMessage, recipients: list[UUID]) -> None: ...
