from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field, RootModel

EXAMPLE = {
    date(2020, 6, 1): [
        {
            "cargo_type": "Glass",
            "rate": Decimal("0.04"),
        },
        {
            "cargo_type": "Other",
            "rate": Decimal("0.01"),
        },
    ],
    date(2020, 7, 1): [
        {
            "cargo_type": "Glass",
            "rate": Decimal("0.035"),
        },
        {
            "cargo_type": "Other",
            "rate": Decimal("0.015"),
        },
    ],
}


class RateItemModel(BaseModel):
    cargo_type: str = Field(examples=["Glass", "Other"])
    rate: Decimal = Field(examples=["0.01", "0.015"])


class RatesModel(RootModel):
    root: dict[date, list[RateItemModel]] = Field(examples=[EXAMPLE])


class RateQuery(BaseModel):
    """
    Запрос тарифа на стоимость
    """

    date_rate: date = Field(examples=[date(2024, 1, 1)])
    cargo_type: str = Field(examples=["Glass"])
    cost: Decimal = Field(examples=["0.01"])


class RateResponse(BaseModel):
    """
    Ответ на запрос
    """

    tariff: Decimal = Field(examples=["0.01"])


class Message(BaseModel):
    detail: str = Field(examples=["message"])


class _BaseRateModel(BaseModel):
    """
    Тариф на стоимость
    """

    date_rate: date = Field(examples=[date(2024, 1, 1)])
    cargo_type: str = Field(examples=["Glass", "Other"])
    rate: Decimal = Field(examples=["0.01", "0.015"])


class GetRateModel(_BaseRateModel):
    """
    Тариф на стоимость
    """

    rate_id: int = Field(examples=[1, 2, 4])


class CreateRateModel(_BaseRateModel):
    """
    Тариф на стоимость
    """

    pass


class UpdateRateModel(_BaseRateModel):
    """
    Тариф на стоимость
    """

    pass
