from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.async_db import async_engine
from src.database.base import Base
from src.database.sync_db import engine


async def ping_db(session: AsyncSession) -> bool:
    try:
        await session.execute(select(text("1")))
    except:  # noqa
        return False
    return True


async def async_create_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def async_drop_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def drop_tables() -> None:
    Base.metadata.drop_all(bind=engine)
