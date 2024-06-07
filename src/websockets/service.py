from dataclasses import dataclass

from aiokafka import AIOKafkaProducer

from uuid import UUID

from src.schemas import NewMessage
from src.config import settings
from .utils import get_topic_name


@dataclass(kw_only=True)
class ProducerService:
    producer: AIOKafkaProducer
    async def send_message(self, message: NewMessage, recipients: list[UUID]) -> None:
        await self.producer.start()
        for recipient in recipients:
            await self.producer.send_and_wait(
                topic=get_topic_name(recipient),
                value=message.model_dump_json().encode(),
            )

producer_service = ProducerService(
    producer=AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BROKER_URL)
)
