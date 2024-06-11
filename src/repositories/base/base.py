from abc import ABC, abstractmethod
from typing import Any


class Repository[T](ABC):
    @abstractmethod
    async def add(self, item: dict[str, Any]) -> T: ...

    @abstractmethod
    async def get(self, id: T) -> dict[str, Any] | None: ...

    @abstractmethod
    async def update(self, id: T, new_values: dict[str, Any]) -> dict[str, Any]: ...

    @abstractmethod
    async def delete(self, id: T) -> int: ...
