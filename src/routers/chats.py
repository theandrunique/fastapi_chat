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
    user: UserAuthorization, chats_service=Provide(Container.ChatsService), users_service=Provide(Container.UsersService),
):
    chats = await chats_service.get_user_chats(user.id)
    for chat in chats:
        if chat.type == ChatType.PRIVATE:
            chat_with = await users_service.get(chat.members[0] if chat.members[0] != user.id else chat.members[1])
            if not chat_with:
                raise Exception()

            chat.id = chat_with.id
            chat.name = chat_with.username
            chat.image_url = chat_with.image_url
    
    chats = [chat for chat in chats if chat.message_count != 0]

    return {
        "chats": chats,
    }
