from typing import Any
from src.mongo import Repository, db
from src.schemas import ChatType, UserChat


class UserChatsRepository(Repository):
    def __init__(self, user_id: str) -> None:
        """
        Initializes the UserChatsRepository with the given user_id.
        
        Parameters:
            user_id (str): The unique identifier of the user.
        
        Returns:
            None
        """
        self.collection = db[f"user_{user_id}_chats"]
    
    async def add(self, chat_id: str, type: ChatType) -> None:
        """
        Inserts a new chat ID into the collection.

        Args:
            chat_id (Any): The ID of the chat to be inserted.

        Returns:
            None: This function does not return anything.
        """
        await self.collection.insert_one({
            "chat_id": chat_id,
            "type": type.value,
        })
    
    async def get(self, chat_id: str) -> UserChat | None:
        result = await self.collection.find_one({"chat_id": chat_id})
        if result:
            return UserChat(**result)
        return None

    async def get_many(self) -> list[UserChat]:
        """
        Asynchronously retrieves a list of all the chat IDs associated with the user.

        Returns:
            list[str]: A list of all the chat IDs associated with the user.
        """
        return [UserChat(**chat) for chat in await self.collection.find().to_list(None)]

    async def delete(self, chat_id: str) -> None:
        raise NotImplementedError()
    
    async def update(self, chat_id: str, new_values: dict[str, Any]) -> None:
        raise NotImplementedError()
