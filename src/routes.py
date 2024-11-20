from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

import models
import services
from src.database.async_db import get_async_db
from src.services import RateItem

FAKE_RATES: dict[date, list[models.RateItemModel]] = {}

router = APIRouter()


@router.get(
    path="/rates",
    status_code=status.HTTP_200_OK,
    response_model=models.RatesModel,
)
async def rates(
    session: AsyncSession = Depends(get_async_db),
) -> models.RatesModel:
    return (await services.get_rates(session=session)).model_dump()


@router.post(
    path="/rates",
    status_code=status.HTTP_201_CREATED,
    response_model=models.Message,
)
async def add_rates(
    data: models.RatesModel,
    session: AsyncSession = Depends(get_async_db),
) -> models.Message:
    return await services.add_rates(
        [
            RateItem(key, item.cargo_type.lower(), item.rate)
            for key, value in data.root.items()
            for item in value
        ],
        session=session,
    )


@router.get(
    path="/tariff",
    status_code=status.HTTP_200_OK,
    response_model=models.RateResponse,
)
async def tariff(
    param: Annotated[models.RateQuery, Query()],
    session: AsyncSession = Depends(get_async_db),
) -> models.RateResponse:
    return await services.get_tariff(
        rate_date=param.date,
        cargo_type=param.cargo_type,
        cost=param.cost,
        session=session,
    )
