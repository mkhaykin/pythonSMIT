import asyncio
from logging import getLogger

import aiokafka

from src.settings import settings

logger = getLogger(__name__)
loop = asyncio.get_event_loop()


async def run_consumer() -> None:
    logger.info("run_consumer")

    consumer = aiokafka.AIOKafkaConsumer(
        settings.KAFKA_TOPIC,
        loop=loop,
        bootstrap_servers=f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}",
        group_id=settings.KAFKA_CONSUMER_GROUP,
    )

    try:
        await consumer.start()
    except Exception as e:
        logger.error(e)
        return

    try:
        async for msg in consumer:
            logger.info(msg)
    finally:
        await consumer.stop()
