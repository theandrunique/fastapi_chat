import json
from aiokafka import AIOKafkaConsumer
from fastapi import APIRouter
from fastapi.websockets import WebSocket, WebSocketDisconnect
from src.logger import logger
from src.config import settings
from src.schemas import Message


router = APIRouter()


@router.websocket("/ws-out/{user_id}")
async def websocket_out(websocket: WebSocket, user_id: str):
    await websocket.accept()

    consumer = AIOKafkaConsumer(
        f"user_{user_id}",
        bootstrap_servers=settings.KAFKA_BROKER_URL,
        group_id="user-group",
    )
    await consumer.start()
    try:
        async for message in consumer:
            msg = Message(**json.loads(message.value.decode("utf-8")))

            await websocket.send_text(msg.model_dump_json())

    except WebSocketDisconnect:
        ...
    except Exception as e:
        logger.error(e)
    finally:
        await consumer.stop()