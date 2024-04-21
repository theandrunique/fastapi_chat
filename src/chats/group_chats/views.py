from fastapi import APIRouter

from .schemas import ChatCreateDefaultValues, ChatCreate

from .repository import GroupChatsRepository
from src.dependencies import UserAuthorization
from src.user_chats_repo import UserChatsRepository

router = APIRouter()


repository = GroupChatsRepository()

@router.post("/")
async def create_group_chat(data: ChatCreate, user: UserAuthorization):
    chat = ChatCreateDefaultValues(name=data.name)
    new_chat = await repository.add(chat)
    user_chats = UserChatsRepository(user.sub)
    await user_chats.add(new_chat.id)
    return new_chat
