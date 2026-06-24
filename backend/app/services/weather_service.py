from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import WeatherSearchNotFoundError
from app.integrations import open_meteo
from app.models.weather_search import WeatherSearch
from app.schemas.weather import (
    CurrentWeatherResponse,
    WeatherSearchCreate,
    WeatherSearchListResponse,
    WeatherSearchResponse,
    WeatherSearchUpdate,
)


async def get_current_weather(
    location: str | None,
    lat: float | None,
    lon: float | None,
) -> CurrentWeatherResponse:
    if lat is not None and lon is not None:
        resolved = f"{lat:.4f}, {lon:.4f}"
    else:
        lat, lon, resolved = await open_meteo.geocode(location or "")

    current, forecast = await open_meteo.get_forecast(lat, lon)
    aqi = await open_meteo.get_aqi(lat, lon)

    current.aqi = aqi.aqi
    current.aqi_label = aqi.label

    return CurrentWeatherResponse(
        resolved_location=resolved,
        latitude=lat,
        longitude=lon,
        current=current,
        forecast=forecast,
    )


async def create_weather_search(
    payload: WeatherSearchCreate,
    db: Session,
) -> WeatherSearchResponse:
    lat, lon, resolved = await open_meteo.geocode(payload.location_query)
    current, _ = await open_meteo.get_forecast(lat, lon, payload.start_date, payload.end_date)

    record = WeatherSearch(
        location_query=payload.location_query,
        resolved_location_name=resolved,
        latitude=Decimal(str(lat)),
        longitude=Decimal(str(lon)),
        start_date=payload.start_date,
        end_date=payload.end_date,
        weather_condition=current.condition,
        temperature=Decimal(str(current.temperature)),
        humidity=current.humidity,
        wind_speed=Decimal(str(current.wind_speed)) if current.wind_speed is not None else None,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return WeatherSearchResponse.model_validate(record)


def list_weather_searches(
    db: Session,
    limit: int = 20,
    offset: int = 0,
) -> WeatherSearchListResponse:
    total = db.scalar(select(func.count()).select_from(WeatherSearch)) or 0
    rows = db.scalars(
        select(WeatherSearch).order_by(WeatherSearch.created_at.desc()).limit(limit).offset(offset)
    ).all()
    return WeatherSearchListResponse(
        total=total,
        items=[WeatherSearchResponse.model_validate(r) for r in rows],
    )


def get_weather_search(record_id: int, db: Session) -> WeatherSearchResponse:
    row = db.get(WeatherSearch, record_id)
    if row is None:
        raise WeatherSearchNotFoundError(f"Weather search {record_id} not found")
    return WeatherSearchResponse.model_validate(row)


async def update_weather_search(
    record_id: int,
    payload: WeatherSearchUpdate,
    db: Session,
) -> WeatherSearchResponse:
    row = db.get(WeatherSearch, record_id)
    if row is None:
        raise WeatherSearchNotFoundError(f"Weather search {record_id} not found")

    new_location = payload.location_query or row.location_query
    new_start = payload.start_date or row.start_date
    new_end = payload.end_date or row.end_date

    lat, lon, resolved = await open_meteo.geocode(new_location)
    current, _ = await open_meteo.get_forecast(lat, lon, new_start, new_end)

    row.location_query = new_location
    row.resolved_location_name = resolved
    row.latitude = Decimal(str(lat))
    row.longitude = Decimal(str(lon))
    row.start_date = new_start
    row.end_date = new_end
    row.weather_condition = current.condition
    row.temperature = Decimal(str(current.temperature))
    row.humidity = current.humidity
    row.wind_speed = Decimal(str(current.wind_speed)) if current.wind_speed is not None else None

    db.commit()
    db.refresh(row)
    return WeatherSearchResponse.model_validate(row)


def delete_weather_search(record_id: int, db: Session) -> None:
    row = db.get(WeatherSearch, record_id)
    if row is None:
        raise WeatherSearchNotFoundError(f"Weather search {record_id} not found")
    db.delete(row)
    db.commit()
