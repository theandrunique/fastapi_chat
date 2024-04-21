from fastapi import APIRouter
from src.chats.dependencies import ExistedChat
from src.chats.exceptions import ChatNotFound
from src.schemas import ChatType
from .schemas import ChatsCollection
from src.dependencies import UserAuthorization
from src.mongo.object_id import PyObjectId
from src.user_chats_repo import UserChatsRepository
from .group_chats.repository import GroupChatsRepository
from .private_chats.repository import PrivateChatsRepository

router = APIRouter()


group_chats_repo = GroupChatsRepository()
private_chats_repo = PrivateChatsRepository()


@router.get("/")
async def get_chats(user: UserAuthorization):
    user_chats = UserChatsRepository(user.sub)
    result = await user_chats.get_many()
    chats = []
    for chat in result:
        if chat.type is ChatType.GROUP:
            await group_chats_repo.get(chat.chat_id)
        if chat.type is ChatType.PRIVATE:
            await private_chats_repo.get(chat.chat_id)

    return ChatsCollection(
        chats=chats
    )

@router.post("/{chat_id}/send-message")
async def send_message(chat: ExistedChat, user: UserAuthorization):
    ...


@router.post("/{user_id}/send-private-message")
async def send_private_message(chat: ExistedPrivateChat, user: UserAuthorization):
    ...

# @router.get("/{chat_id}")
# async def get_chat(chat_id: PyObjectId):
    # found_chat = await repository.get(chat_id)
    # if not found_chat:
        # raise ChatNotFound()
    # return found_chat


@router.delete("/{chat_id}")
async def delete_chat(chat_id: PyObjectId):
    ...
