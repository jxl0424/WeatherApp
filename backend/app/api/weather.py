from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.weather import (
    CurrentWeatherResponse,
    WeatherSearchCreate,
    WeatherSearchListResponse,
    WeatherSearchResponse,
    WeatherSearchUpdate,
)
from app.services import weather_service

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/current", response_model=CurrentWeatherResponse)
async def current_weather(
    location: str | None = Query(default=None),
    lat: float | None = Query(default=None),
    lon: float | None = Query(default=None),
) -> CurrentWeatherResponse:
    return await weather_service.get_current_weather(location, lat, lon)


@router.post("", response_model=WeatherSearchResponse, status_code=201)
async def create_search(
    payload: WeatherSearchCreate,
    db: Session = Depends(get_db),
) -> WeatherSearchResponse:
    return await weather_service.create_weather_search(payload, db)


@router.get("", response_model=WeatherSearchListResponse)
def list_searches(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> WeatherSearchListResponse:
    return weather_service.list_weather_searches(db, limit, offset)


@router.get("/{record_id}", response_model=WeatherSearchResponse)
def get_search(record_id: int, db: Session = Depends(get_db)) -> WeatherSearchResponse:
    return weather_service.get_weather_search(record_id, db)


@router.put("/{record_id}", response_model=WeatherSearchResponse)
async def update_search(
    record_id: int,
    payload: WeatherSearchUpdate,
    db: Session = Depends(get_db),
) -> WeatherSearchResponse:
    return await weather_service.update_weather_search(record_id, payload, db)


@router.delete("/{record_id}", status_code=204)
def delete_search(record_id: int, db: Session = Depends(get_db)) -> Response:
    weather_service.delete_weather_search(record_id, db)
    return Response(status_code=204)
