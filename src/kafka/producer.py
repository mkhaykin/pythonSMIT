import asyncio
import json
from datetime import datetime
from logging import getLogger

import aiokafka

from src.settings import settings

logger = getLogger(__name__)

loop = asyncio.get_event_loop()


async def send_log(user: str | None, action: str, message: dict | None = None) -> None:
    if user is None:
        user = "unknown"
    if message is None:
        message = {}

    producer = aiokafka.AIOKafkaProducer(
        loop=loop,
        bootstrap_servers=f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}",
    )

    try:
        await producer.start()
    except Exception as e:
        logger.error(e)
        return

    try:
        json_value = json.dumps(
            {
                "user": user,
                "action": action,
                "message": message,
                "timestamp": str(datetime.now()),
            },
        ).encode("utf-8")
        await producer.send(settings.KAFKA_TOPIC, value=json_value)
    finally:
        await producer.stop()
