from typing import Annotated
from uuid import UUID

from fastapi import Depends
from src.mongo.object_id import PyObjectId
from src.security.dependencies import UserAuthorization

from .service import chats_service
from .exceptions import ChatNotFound
from .schemas import Chat, ChatFactory, ChatType


async def get_existed_group_chat(chat_id: PyObjectId) -> Chat:
    chat = await chats_service.get(chat_id)
    if not chat:
        raise ChatNotFound(str(chat_id))
    return chat


ExistedGroupChat = Annotated[Chat, Depends(get_existed_group_chat)]


async def get_existed_chat(
    chat_id: PyObjectId | UUID, payload: UserAuthorization
) -> Chat:
    if isinstance(chat_id, PyObjectId):
        chat = await chats_service.get(chat_id)
    elif isinstance(chat_id, UUID):
        user_id = chat_id
        sender_id = payload.sub
        chat = await chats_service.get_private_chat(user_id, sender_id)
        if not chat:
            chat = await chats_service.add(
                ChatFactory(type=ChatType.PRIVATE, members=[user_id, sender_id])
            )

    if not chat:
        raise ChatNotFound(str(chat_id))
    return chat


ExistedChat = Annotated[Chat, Depends(get_existed_chat)]
