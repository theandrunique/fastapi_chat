from aiokafka import AIOKafkaProducer
import punq
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.services.base.base_chats import ChatsService
from src.services.chats import ImplChatsService
from src.services.jwt import PyJWTService
from src.services.users import ImplUsersService
from src.services.auth import ImplAuthService
from src.services.messages import ImplMessagesService
from src.services.base.base_auth import AuthService
from src.services.base.base_jwt import JWTService
from src.services.base.base_users import UsersService
from src.services.base.base_messages import MessagesService
from src.repositories.base.base_chats import ChatsRepository
from src.repositories.base.base_messages import MessagesRepository
from src.repositories.chats import MongoChatsRepository
from src.repositories.messages import MongoMessagesRepository
from src.services.base.base_producer import ProducerService
from src.services.producer import ImplProducerService

from src.config import settings


def init_container() -> punq.Container:
    container = punq.Container()

    client = AsyncIOMotorClient(
        settings.MONGO.URI.unicode_string(),
        uuidRepresentation="standard",
        serverSelectionTimeoutMS=5000,
    )

    container.register(
        AsyncIOMotorDatabase,
        instance=client[settings.MONGO.DATABASE_NAME],
    )

    container.register(
        UsersService,
        instance=ImplUsersService(
            auth_service_url=settings.SECURITY.AUTHORIZATION_SERVER_URL
        ),
    )

    container.register(
        AuthService,
        ImplAuthService,
        scope=punq.Scope.singleton,
    )

    container.register(
        JWTService,
        instance=PyJWTService(
            auth_server_url=settings.SECURITY.AUTHORIZATION_SERVER_URL,
            client_id=settings.SECURITY.CLIENT_ID,
            algorithm=settings.SECURITY.ALGORITHM,
        ),
    )

    container.register(
        MessagesService,
        factory=lambda chat_id: ImplMessagesService(
            repository=container.resolve(MessagesRepository, chat_id=chat_id) # type: ignore
        ),
    )

    container.register(
        ChatsService, 
        ImplChatsService,
        scope=punq.Scope.singleton,
    )

    container.register(
        ChatsRepository,
        instance=MongoChatsRepository(
            collection=container.resolve(AsyncIOMotorDatabase)["chats"] # type: ignore
        )
    )

    container.register(
        MessagesRepository,
        factory=lambda chat_id: MongoMessagesRepository(
            collection=container.resolve(AsyncIOMotorDatabase)[str(chat_id)] # type: ignore
        )
    )

    container.register(
        ProducerService,
        instance=ImplProducerService(
            producer=AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BROKER_URL)
        ),
    )

    return container


container = init_container()
