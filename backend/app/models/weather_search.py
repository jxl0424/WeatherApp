from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Date, Index, Numeric, SmallInteger, String
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class WeatherSearch(Base):
    __tablename__ = "weather_searches"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    location_query: Mapped[str] = mapped_column(String(255), nullable=False)
    resolved_location_name: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[Decimal] = mapped_column(Numeric(8, 5), nullable=False)
    longitude: Mapped[Decimal] = mapped_column(Numeric(8, 5), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    weather_condition: Mapped[str] = mapped_column(String(64), nullable=False)
    temperature: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    humidity: Mapped[int | None] = mapped_column(SmallInteger)
    wind_speed: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        Index("ix_weather_searches_created_at", "created_at"),
        Index("ix_weather_searches_resolved_location_name", "resolved_location_name"),
    )
