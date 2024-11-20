from datetime import date
from decimal import Decimal

from sqlalchemy import BigInteger, Date, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class Rate(Base):
    __tablename__ = "rates"

    rate_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    rate_date: Mapped[date] = mapped_column(
        Date,
        index=True,
        unique=False,
        nullable=False,
    )

    cargo_type: Mapped[str] = mapped_column(
        String,
        index=True,
        unique=False,
        nullable=False,
    )

    rate_value: Mapped[Decimal] = mapped_column(
        Numeric(10, 4),
        index=False,
        unique=False,
        nullable=False,
    )

    __table_args__ = (UniqueConstraint("rate_date", "cargo_type", name="uc_rate"),)
