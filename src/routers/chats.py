from fastapi import APIRouter

from src.models.chat import Chat, ChatType
from src.schemas.chats import ChatCreate, ChatFactory

from src.dependencies import Container, Provide, UserAuthorization


router = APIRouter()


@router.post("")
async def create_group_chat(
    chat: ChatCreate,
    user: UserAuthorization,
    chats_service=Provide(Container.ChatsService),
) -> Chat:
    new_chat = ChatFactory(
        name=chat.name,
        creator_id=user.id,
        type=ChatType.GROUP,
        members=[user.id],
    )
    return await chats_service.add(new_chat)


@router.get("")
async def get_chats(
    user: UserAuthorization, chats_service=Provide(Container.ChatsService)
):
    chats = await chats_service.get_user_chats(user.id)
    return {
        "chats": chats,
    }
