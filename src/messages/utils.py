from src.mongo.object_id import PyObjectId
from src.mongo.client import db

from .repository import MessagesRepository
from .service import MessagesService


def get_messages_service(chat_id: PyObjectId) -> MessagesService:
    service = MessagesService(
        repository=MessagesRepository(collection=db[str(chat_id)])
    )
    return service
