from typing import Annotated
from uuid import UUID
from fastapi import Depends, params
from fastapi.security import OAuth2PasswordBearer

from src.container import container
from src.exceptions import ChatNotFound, InvalidToken, UserNotFound
from src.models.chat import Chat
from src.models.user import User
from src.schemas.object_id import PyObjectId
from src.services.base.base_auth import AuthService
from src.services.base.base_jwt import JWTService
from src.services.base.base_users import UsersService
from src.services.base.base_chats import ChatsService
from src.services.base.base_messages import MessagesService
from src.services.base.base_producer import ProducerService


class Container:
    UsersService = UsersService
    AuthService = AuthService
    JWTService = JWTService
    ChatsService = ChatsService
    MessagesService = MessagesService
    ProducerService = ProducerService


def Provide[T](
    dependency: type[T],
) -> T:
    def _dependency():
        return container.resolve(dependency)

    return params.Depends(dependency=_dependency, use_cache=True)  # type: ignore


def factory[T](dependency: type[T], **kwargs) -> T:
    return container.resolve(dependency, **kwargs) # type: ignore


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="",
    auto_error=False,
)


async def user_authentication(
    token: str = Depends(oauth2_scheme),
    auth_service=Provide(Container.AuthService),
) -> User:
    user = await auth_service.authenticate(token)
    if not user:
        raise InvalidToken()
    return user


UserAuthorization = Annotated[User, Depends(user_authentication)]


async def get_existed_group_chat(chat_id: PyObjectId, chats_service=Provide(Container.ChatsService)) -> Chat:
    chat = await chats_service.get(chat_id)
    if not chat:
        raise ChatNotFound(str(chat_id))
    return chat


ExistedGroupChat = Annotated[Chat, Depends(get_existed_group_chat)]


async def get_existed_private_chat(
    user_id: UUID, user: UserAuthorization, chats_service=Provide(Container.ChatsService),
    users_service = Provide(Container.UsersService),
) -> tuple[User, Chat]:
    receiver = await users_service.get(user_id)
    if not receiver:
        raise UserNotFound(str(user_id))
    chat = await chats_service.get_private_chat(receiver.id, user.id)
    return receiver, chat


ExistedPrivateChat = Annotated[tuple[User, Chat], Depends(get_existed_private_chat)]
