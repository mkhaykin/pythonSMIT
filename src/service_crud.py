from logging import getLogger

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.database.models import Rate
from src.database.utils import db_error_wrapper
from src.models import CreateRateModel, UpdateRateModel

logger = getLogger(__name__)


@db_error_wrapper
async def get_rate(
    item_id: int,
    *,
    session: AsyncSession,
) -> models.GetRateModel:
    rate: Rate | None = await session.get(Rate, item_id)
    if not rate:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Ставка с id = {item_id} не найдена.",
        )

    return models.GetRateModel(
        rate_id=rate.rate_id,
        date_rate=rate.rate_date,
        cargo_type=rate.cargo_type,
        rate=rate.rate_value,
    )


@db_error_wrapper
async def add_rate(
    item: CreateRateModel,
    *,
    session: AsyncSession,
) -> models.GetRateModel:
    rate = Rate(
        rate_date=item.date_rate,
        cargo_type=item.cargo_type,
        rate_value=item.rate,
    )

    session.add(rate)
    await session.commit()
    await session.refresh(rate)

    return models.GetRateModel(
        rate_id=rate.rate_id,
        date_rate=rate.rate_date,
        cargo_type=rate.cargo_type,
        rate=rate.rate_value,
    )


@db_error_wrapper
async def edit_rate(
    item_id: int,
    item: UpdateRateModel,
    *,
    session: AsyncSession,
) -> models.GetRateModel:
    rate: Rate | None = await session.get(Rate, item_id)
    if not rate:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Ставка с id = {item_id} не найдена.",
        )

    rate.rate_date = item.date_rate
    rate.cargo_type = item.cargo_type
    rate.rate_value = item.rate

    await session.commit()
    await session.refresh(rate)

    return models.GetRateModel(
        rate_id=rate.rate_id,
        date_rate=rate.rate_date,
        cargo_type=rate.cargo_type,
        rate=rate.rate_value,
    )


@db_error_wrapper
async def delete_rate(
    item_id: int,
    *,
    session: AsyncSession,
) -> models.Message:
    rate: Rate | None = await session.get(Rate, item_id)
    if not rate:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Ставка с id = {item_id} не найдена.",
        )

    await session.delete(rate)
    await session.commit()

    return models.Message(detail=f"Ставка с id = {item_id} удалена.")
