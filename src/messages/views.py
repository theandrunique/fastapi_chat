from fastapi import APIRouter
from pydantic import PositiveInt, NonNegativeInt

from src.chats.dependencies import ExistedChat
from src.chats.service import chats_service
from src.security.dependencies import UserAuthorization
from src.websockets.service import producer_service
from src.schemas import NewMessage

from .utils import get_messages_service
from .factories import MessageFactory
from .schemas import MessageCreate

router = APIRouter()


@router.get("")
async def get_messages(
    chat: ExistedChat,
    count: PositiveInt = 20,
    offset: NonNegativeInt = 0,
):
    messages_service = get_messages_service(chat.id)
    messages = await messages_service.get_many(count, offset)
    return {
        "chat": chat,
        "messages": messages,
    }


@router.post("")
async def send_message(
    message: MessageCreate,
    chat: ExistedChat,
    payload: UserAuthorization,
):
    messages_service = get_messages_service(chat.id)
    new_message = await messages_service.add(
        MessageFactory(
            id=chat.message_count,
            text=message.text,
            from_id=payload.sub,
            attachments=message.attachments,
        )
    )
    await chats_service.update_last_message(chat_id=chat.id, new_message=new_message)
    chat.last_message = new_message
    new_message =NewMessage(
        chat=chat,
        message=new_message,
    )
    await producer_service.send_message(message=new_message, recipients=chat.members)
    return new_message
