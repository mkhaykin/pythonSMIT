from datetime import date
from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Query

import models

FAKE_RATES: dict[date, list[models.RateItemModel]] = {}

router = APIRouter()


@router.get(
    path="/rates",
    status_code=status.HTTP_200_OK,
    response_model=models.RatesModel,
)
async def rates() -> models.RatesModel:
    return models.RatesModel(FAKE_RATES)


@router.post(
    path="/rates",
    status_code=status.HTTP_201_CREATED,
    response_model=models.Message,
)
async def add_rates(
    data: models.RatesModel,
) -> models.Message:
    FAKE_RATES.clear()
    FAKE_RATES.update(data.root)
    return models.Message(detail="ok")


@router.get(
    path="/rate",
    status_code=status.HTTP_200_OK,
    response_model=models.RateQuery,
)
async def rate(
    param: Annotated[models.RateQuery, Query()],
) -> models.RateResponse:
    print(param)
    result_rates: list[models.RateItemModel] | None = None

    for _date in sorted(FAKE_RATES):
        if _date > param.date:
            break
        result_rates = FAKE_RATES[_date]

    if result_rates is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Нет действующего тарифа.",
        )

    for item in result_rates:
        if item.cargo_type == param.cargo_type:
            return models.RateResponse(
                rate=item.rate,
            )

    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        "Нет действующего тарифа.",
    )
