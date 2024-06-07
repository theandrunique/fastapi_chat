from typing import Any

from pymongo import DESCENDING
from src.mongo.base_repository import BaseMongoRepository


class MessagesRepository(BaseMongoRepository[int]):
    async def get_many(self, count: int, offset: int) -> list[dict[str, Any]]:
        result = await self.collection.find().sort("_id", DESCENDING).skip(offset).to_list(length=count)
        result.reverse()
        return result
