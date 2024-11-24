import asyncio
import logging

from fastapi import FastAPI

from src.database.utils import create_tables
from src.kafka.consumer import run_consumer
from src.routes import router
from src.routes_crud import router as crud_router

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

create_tables()

app = FastAPI()
app.include_router(router)
app.include_router(crud_router, prefix="/rate")

loop = asyncio.get_event_loop()


@app.on_event("startup")
async def startup_event() -> None:
    logger.info("startup")
    loop.create_task(run_consumer())
