import datetime
from typing import Any
from src.mongo import Repository, db
from src.mongo.object_id import PyObjectId
from src.schemas import Message
from .utils import get_chat_id


class PrivateMessengerRepository(Repository):
    def __init__(self, from_id: str, to_id: str) -> None:
        collection_name = get_chat_id(from_id, to_id)
        self.collection = db[collection_name]
        self.user_id = from_id
     
    async def add(self, text: str) -> Message:
        message_count = await self.collection.count_documents({})
        new_message = Message(
            text=text,
            sended_at=datetime.datetime.now(datetime.UTC),
            from_id=self.user_id,
            message_id=message_count + 1
        )
        await self.collection.insert_one(new_message.model_dump())
        return new_message
    
    async def get_many(self, count: int, offset: int) -> list[Message]:
        result = await self.collection.find().sort("message_id", -1).skip(offset).limit(count).to_list(None)
        return [Message(**message) for message in result]

    async def delete(self, id: PyObjectId) -> int:
        raise NotImplementedError()
    
    async def update(self, id: PyObjectId, new_values: dict[str, Any]) -> Any:
        raise NotImplementedError()
    
    async def get(self, id: PyObjectId) -> Any:
        raise NotImplementedError()
