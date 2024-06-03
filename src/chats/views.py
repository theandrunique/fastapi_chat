from fastapi import APIRouter

from src.security.dependencies import UserAuthorization

from .schemas import Chat, ChatCreate, ChatFactory, ChatType
from .service import chats_service


router = APIRouter()


@router.post("")
async def create_chat(new_chat: ChatCreate, payload: UserAuthorization) -> Chat:
    new_chat = ChatFactory(
        name=new_chat.name,
        creator_id=payload.sub,
        type=ChatType.GROUP,
        members=[payload.sub],
    )
    return await chats_service.add(new_chat)


@router.get("")
async def get_chats(payload: UserAuthorization):
    chats = await chats_service.get_user_chats(payload.sub)
    return {
        "chats": chats,
    }
