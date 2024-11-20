from datetime import date
from decimal import Decimal
from logging import getLogger

from fastapi import HTTPException, status
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import NamedTuple

from src import models
from src.database.models import Rate
from src.database.utils import db_error_wrapper
from src.models import RateItemModel

logger = getLogger(__name__)


class RateItem(NamedTuple):
    date: date
    cargo_type: str
    rate: Decimal


@db_error_wrapper
async def add_rates(
    data: list[RateItem],
    *,
    session: AsyncSession,
) -> models.Message:
    await session.execute(delete(Rate))  # or TRUNCATE TABLE ...
    await session.execute(
        insert(Rate),
        [
            {
                "rate_date": item.date,
                "cargo_type": item.cargo_type,
                "rate_value": item.rate,
            }
            for item in data
        ],
    )
    await session.commit()

    return models.Message(detail="ok")


@db_error_wrapper
async def get_rates(
    *,
    session: AsyncSession,
) -> models.RatesModel:
    result: dict[date, list[RateItemModel]] = {}

    rows = await session.execute(select(Rate))
    for row in rows:
        result.setdefault(row.Rate.rate_date, []).append(
            models.RateItemModel(
                cargo_type=row.Rate.cargo_type.capitalize(),
                rate=row.Rate.rate_value,
            ),
        )

    return models.RatesModel(result)


@db_error_wrapper
async def get_tariff(
    rate_date: date,
    cargo_type: str,
    cost: Decimal,
    *,
    session: AsyncSession,
) -> models.RateResponse:
    stmt = (
        select(Rate.rate_value)
        .where(Rate.cargo_type == cargo_type.lower(), Rate.rate_date <= rate_date)
        .order_by(Rate.rate_date.desc())
        .limit(1)
    )

    if result := (await session.execute(stmt)).one_or_none():
        return models.RateResponse(
            tariff=result.rate_value * cost,
        )

    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        "Нет действующего тарифа.",
    )
