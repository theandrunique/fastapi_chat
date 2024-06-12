from fastapi import APIRouter
from pydantic import PositiveInt, NonNegativeInt

from src.dependencies import ExistedPrivateChat, Provide, UserAuthorization, Container, factory
from src.schemas.messages import MessageCreate
from src.schemas.messages import MessageFactory
from src.schemas.messages import NewMessage


router = APIRouter()


@router.get("")
async def get_messages(
    receiver_with_chat: ExistedPrivateChat,
    count: PositiveInt = 20,
    offset: NonNegativeInt = 0,
):
    receiver, chat = receiver_with_chat

    messages_service = factory(Container.MessagesService, chat_id=chat.id)
    messages = await messages_service.get_many(count, offset)
    chat.id = receiver.id
    chat.name = receiver.username
    
    return {
        "chat": chat,
        "messages": messages,
    }


@router.post("")
async def send_message(
    receiver_with_chat: ExistedPrivateChat,
    message: MessageCreate,
    user: UserAuthorization,
    chats_service = Provide(Container.ChatsService),
    producer_service = Provide(Container.ProducerService),
):
    receiver, chat = receiver_with_chat
    messages_service = factory(Container.MessagesService, chat_id=chat.id)

    new_message = await messages_service.add(
        MessageFactory(
            id=chat.message_count,
            text=message.text,
            from_id=user.id,
            attachments=message.attachments,
        )
    )
    chat = await chats_service.update_last_message(chat_id=chat.id, new_message=new_message)
    chat.last_message = new_message
    new_message = NewMessage(
        chat=chat,
        message=new_message,
    )
    chat.id = user.id
    chat.name = user.username
    await producer_service.send_message(message=new_message, recipients=chat.members)
    
    chat.id = receiver.id
    chat.name = receiver.username
    return new_message
