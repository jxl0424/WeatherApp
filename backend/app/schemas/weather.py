from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator, model_validator


# ── Request schemas ────────────────────────────────────────────────────────────

class WeatherSearchCreate(BaseModel):
    location_query: str = Field(min_length=1, max_length=255)
    start_date: date
    end_date: date

    @field_validator("location_query")
    @classmethod
    def strip_location(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("location_query must not be blank")
        return stripped

    @model_validator(mode="after")
    def validate_date_range(self) -> "WeatherSearchCreate":
        from datetime import timedelta

        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        if (self.end_date - self.start_date).days > 16:
            raise ValueError("Date range cannot exceed 16 days (Open-Meteo forecast limit)")
        return self


class WeatherSearchUpdate(BaseModel):
    location_query: str | None = Field(default=None, min_length=1, max_length=255)
    start_date: date | None = None
    end_date: date | None = None

    @field_validator("location_query")
    @classmethod
    def strip_location(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        if not stripped:
            raise ValueError("location_query must not be blank")
        return stripped

    @model_validator(mode="after")
    def validate_date_range(self) -> "WeatherSearchUpdate":
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValueError("end_date must be on or after start_date")
            if (self.end_date - self.start_date).days > 16:
                raise ValueError("Date range cannot exceed 16 days")
        return self


# ── Response schemas ───────────────────────────────────────────────────────────

class WeatherSearchResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    location_query: str
    resolved_location_name: str
    latitude: Decimal
    longitude: Decimal
    start_date: date
    end_date: date
    weather_condition: str
    temperature: Decimal
    humidity: int | None
    wind_speed: Decimal | None
    created_at: datetime
    updated_at: datetime


class WeatherSearchListResponse(BaseModel):
    total: int
    items: list[WeatherSearchResponse]


# ── Current weather schemas ────────────────────────────────────────────────────

class CurrentWeather(BaseModel):
    temperature: float
    feels_like: float | None = None
    humidity: int | None = None
    wind_speed: float | None = None
    condition: str
    condition_code: int
    aqi: int | None = None
    aqi_label: str | None = None


class ForecastDay(BaseModel):
    date: date
    temp_min: float
    temp_max: float
    condition: str
    condition_code: int
    precipitation_sum: float | None = None
    wind_speed_max: float | None = None


class CurrentWeatherResponse(BaseModel):
    resolved_location: str
    latitude: float
    longitude: float
    current: CurrentWeather
    forecast: list[ForecastDay]


# ── AI advice schemas ──────────────────────────────────────────────────────────

class AdviceRequest(BaseModel):
    location: str
    current: CurrentWeather
    forecast: list[ForecastDay]


class AdviceResponse(BaseModel):
    clothing: list[str] = []
    packing: list[str] = []
    activities: list[str] = []
    travel_considerations: list[str] = []
    warnings: list[str] = []


# ── AQI schema ────────────────────────────────────────────────────────────────

class AQIResponse(BaseModel):
    aqi: int | None
    label: str
    pm2_5: float | None = None
    pm10: float | None = None
