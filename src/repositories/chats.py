from typing import Any
from uuid import UUID

from src.models.chat import ChatType
from src.schemas.object_id import PyObjectId

from .base.base_mongo_repository import BaseMongoRepository
from .base.base_chats import ChatsRepository

class MongoChatsRepository(BaseMongoRepository[PyObjectId], ChatsRepository):
    async def get_user_chats(self, user_id: UUID) -> list[dict[str, Any]]:
        result = await self.collection.find({"members": {"$in": [user_id]}}).to_list(
            None
        )
        return [chat for chat in result]

    async def get_private_chat(
        self, user1_id: UUID, user2_id: UUID
    ) -> dict[str, Any] | None:
        chat = await self.collection.find_one(
            {"type": ChatType.PRIVATE, "members": {"$all": [user1_id, user2_id]}}
        )
        return chat
