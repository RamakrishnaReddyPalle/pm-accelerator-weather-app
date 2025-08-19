# backend/app/models.py
# ORM models for Weather App
from sqlalchemy import Integer, String, Float, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON
from .database import Base

class WeatherHistory(Base):
    __tablename__ = "weather_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Location & coords
    location_name: Mapped[str | None] = mapped_column(String, nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Date range persistence
    start_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[Date | None] = mapped_column(Date, nullable=True)

    # direct reading fields to align with schemas.py
    temperature: Mapped[float | None] = mapped_column(Float, nullable=True)
    humidity: Mapped[float | None] = mapped_column(Float, nullable=True)
    recorded_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # raw payload from OpenWeather
    weather_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Timestamps
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
