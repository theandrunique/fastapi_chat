from typing import Any
from .schemas import ChatCreateDefaultValues
from src.mongo import Repository, db
from src.mongo.object_id import PyObjectId
from src.schemas import Chat



chats_collection = db["group_chats"]

class GroupChatsRepository(Repository):
    def __init__(self) -> None:
        pass

    async def add(self, item: ChatCreateDefaultValues) -> Chat:
        result = await chats_collection.insert_one(item.model_dump())
        new_chat = Chat(
            id=result.inserted_id,
            **item.model_dump(),
        )
        return new_chat

    async def get(seld, id: PyObjectId) -> Chat | None:
        result = await chats_collection.find_one({"_id": id})
        if result:
            return Chat(**result)
    
    async def get_many(self, count: int, offset: int) -> list[Any]:
        raise NotImplementedError()
    
    async def update(self, id: PyObjectId, new_values: dict[str, Any]) -> Any:
        raise NotImplementedError()

    async def delete(self, id: PyObjectId) -> int:
        result = await chats_collection.delete_one({"_id": id})
        return result.deleted_count
 
