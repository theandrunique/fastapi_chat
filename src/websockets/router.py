import json
from aiokafka import AIOKafkaConsumer
from fastapi import APIRouter, status
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.exceptions import WebSocketException
from src.logger import logger
from src.config import settings
from src.schemas import NewMessage
from src.security.utils import decode_payload
from src.websockets.utils import get_topic_name


router = APIRouter()


@router.websocket("/updates")
async def websocket_out(
    websocket: WebSocket,
    access_token: str,
):
    payload = decode_payload(access_token)
    if not payload:
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token"
        )

    await websocket.accept()

    consumer = AIOKafkaConsumer(
        get_topic_name(user_id=payload.sub),
        bootstrap_servers=settings.KAFKA_BROKER_URL,
        group_id="user-group",
        enable_auto_commit=False,
    )
    await consumer.start()
    try:
        async for message in consumer:
            msg = NewMessage(**json.loads(message.value.decode("utf-8")))
            await websocket.send_text(msg.model_dump_json())
            await consumer.commit()
    except WebSocketDisconnect:
        ...
    except Exception as e:
        logger.error(e)
    finally:
        await consumer.stop()
