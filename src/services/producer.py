from abc import ABC
from dataclasses import dataclass
from uuid import UUID

from aiokafka import AIOKafkaProducer

from src.schemas.messages import NewMessage
from src.utils import get_topic_name


@dataclass(kw_only=True)
class ImplProducerService(ABC):
    producer: AIOKafkaProducer

    async def send_message(self, message: NewMessage, recipients: list[UUID]) -> None:
        await self.producer.start()
        for recipient in recipients:
            if message.message.from_id != recipient:
                await self.producer.send_and_wait(
                    topic=get_topic_name(recipient),
                    value=message.model_dump_json().encode(),
                )
