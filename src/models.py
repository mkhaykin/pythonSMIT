"""
JSON
{
    "2020-06-01": [
        {
            "cargo_type": "Glass",
            "rate": "0.04"
        },
        {
            "cargo_type": "Other",
            "rate": "0.01"
        }
    ],
    "2020-07-01": [
        {
            "cargo_type": "Glass",
            "rate": "0.035"
        },
        {
            "cargo_type": "Other",
            "rate": "0.015"
        }
    ]
}
"""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, RootModel


class RateItemModel(BaseModel):
    cargo_type: str
    rate: Decimal


class RatesModel(RootModel[dict[date, list[RateItemModel]]]):
    pass


class RateQuery(BaseModel):
    date: date
    cargo_type: str


class RateResponse(BaseModel):
    rate: Decimal


class Message(BaseModel):
    detail: str