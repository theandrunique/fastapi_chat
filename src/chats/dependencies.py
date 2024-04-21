from typing import Annotated

from fastapi import Depends
from src.chats.exceptions import ChatNotFound
from .group_chats.repository import GroupChatsRepository
from .private_chats.repository import PrivateChatsRepository
from src.dependencies import UserAuthorization
from src.mongo.object_id import PyObjectId
from src.schemas import Chat, ChatType, PrivateChat
from src.user_chats_repo import UserChatsRepository


group_chats_repo = GroupChatsRepository()
private_chats_repo = PrivateChatsRepository()

async def get_chat(chat_id: PyObjectId, user: UserAuthorization) -> PrivateChat | Chat:
    user_chats = UserChatsRepository(user.sub)
    chat = await user_chats.get(chat_id)
    if not chat:
        raise ChatNotFound()
    if chat.type is ChatType.GROUP:
        return await group_chats_repo.get(chat_id)
    if chat.type is ChatType.PRIVATE:
        return await private_chats_repo.get(chat_id)
    
    raise Exception("This should not have happen")


ExistedChat = Annotated[PrivateChat | Chat, Depends(get_chat)]


async def get_private_chat()


ExistedPrivateChat = Annotated[PrivateChat, Depends(get_chat)]