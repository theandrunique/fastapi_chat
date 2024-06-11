from abc import ABC, abstractmethod
from uuid import UUID

from src.models.user import User


class UsersService(ABC):
    @abstractmethod
    async def get(self, id: UUID) -> User | None: ...
