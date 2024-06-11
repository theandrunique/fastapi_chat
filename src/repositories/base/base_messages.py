from abc import abstractmethod
from typing import Any

from .base import Repository


class MessagesRepository(Repository[int]):
    @abstractmethod
    async def get_many(self, count: int, offset: int) -> list[dict[str, Any]]: ...
