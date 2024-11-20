from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

import models
import services
from src.database.async_db import get_async_db
from src.services import RateItem

router = APIRouter()


@router.get(
    path="/rates",
    summary="Получить ставки страхования.",
    status_code=status.HTTP_200_OK,
    response_model=models.RatesModel,
    response_description="Полное содержимое БД.",
)
async def rates(
    session: AsyncSession = Depends(get_async_db),
) -> models.RatesModel:
    return (await services.get_rates(session=session)).model_dump()


@router.post(
    path="/rates",
    summary="Переписать ставки страхования новыми данными.",
    status_code=status.HTTP_201_CREATED,
    response_model=models.Message,
    response_description="Результат (текстовое сообщение)",
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
    summary="Получить действующий тариф.",
    status_code=status.HTTP_200_OK,
    response_model=models.RateResponse,
    response_description="Стоимость страхования.",
)
async def tariff(
    param: Annotated[models.RateQuery, Query()],
    session: AsyncSession = Depends(get_async_db),
) -> models.RateResponse:
    return await services.get_tariff(
        rate_date=param.date_rate,
        cargo_type=param.cargo_type,
        cost=param.cost,
        session=session,
    )
