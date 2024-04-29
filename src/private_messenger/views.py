from aiokafka import AIOKafkaProducer
from fastapi import APIRouter

from src.private_messenger.utils import get_chat_id

from .exceptions import ChatNotFound
from src.dependencies import UserAuthorization
from src.config import settings
from src.schemas import ChatType
from src.user_chats_repo import UserChatsRepository
from .repository import PrivateMessengerRepository

from .schemas import MessageCollection, MessageCreate, PrivateChat, PrivateChatsCollection
from src.mongo import db


router = APIRouter()

@router.post("/{user_id}/create")
async def create_private_chat(user_id: str, user: UserAuthorization):
    from_id = user.sub
    to_id = user_id

    user_1 = UserChatsRepository(from_id)
    user_2 = UserChatsRepository(to_id)
    chat_id = get_chat_id(from_id=from_id, to_id=to_id)

    await user_1.add(chat_id=chat_id, type=ChatType.PRIVATE, member_id=to_id)
    await user_2.add(chat_id=chat_id, type=ChatType.PRIVATE, member_id=from_id)
    

@router.post("/{user_id}/send-message")
async def send_private_message(user_id: str, message: MessageCreate, user: UserAuthorization):
    user_chats = UserChatsRepository(user.sub)
    if not await user_chats.get(get_chat_id(from_id=user.sub, to_id=user_id)):
        raise ChatNotFound()

    repository = PrivateMessengerRepository(from_id=user.sub, to_id=user_id)
    new_message = await repository.add(message.text)

    producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BROKER_URL)
    await producer.start()
    try:
        await producer.send_and_wait(f"user_{user_id}", new_message.model_dump_json().encode("utf-8"))
    finally:
        await producer.stop()
    return new_message


@router.get("/{user_id}/")
async def get_private_messages(user_id: str, user: UserAuthorization, count: int = 20, offset: int = 0):
    repository = PrivateMessengerRepository(from_id=user.sub, to_id=user_id)
    messages = await repository.get_many(count=count, offset=offset)
    return MessageCollection(
        messages=messages,
    )


@router.get("/")
async def get_chats(user: UserAuthorization):
    user_chats = UserChatsRepository(user.sub)
    result = await user_chats.get_many()
    chats = []
    for item in result:
        collection = db[item.chat_id]
        chat = PrivateChat(
            id=item.chat_id,
            type=item.type,
            messages_count=await collection.count_documents({}),
            last_message=await collection.find_one({}, sort=[("message_id", -1)]),
            member_id=item.member_id,
        )
        chats.append(chat)

    return PrivateChatsCollection(
        chats=chats,
    )
