from typing import Any

from pymongo import DESCENDING
from .base.base_mongo_repository import BaseMongoRepository
from .base.base_messages import MessagesRepository


class MongoMessagesRepository(BaseMongoRepository[int], MessagesRepository):
    async def get_many(self, count: int, offset: int) -> list[dict[str, Any]]:
        result = (
            await self.collection.find()
            .sort("_id", DESCENDING)
            .skip(offset)
            .to_list(length=count)
        )
        result.reverse()
        return result
