from abc import abstractmethod
from typing import Any
from uuid import UUID

from src.schemas.object_id import PyObjectId

from .base import Repository


class ChatsRepository(Repository[PyObjectId]):
    @abstractmethod
    async def get_user_chats(self, user_id: UUID) -> list[dict[str, Any]]: ...

    @abstractmethod
    async def get_private_chat(
        self, user1_id: UUID, user2_id: UUID
    ) -> dict[str, Any] | None: ...
