from fastapi import APIRouter, Depends, Query, Response
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
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


@router.get("/current", response_model=CurrentWeatherResponse, summary="Get current weather by location name or coordinates")
async def current_weather(
    location: str | None = Query(default=None, description="City name, address, or landmark"),
    lat: float | None = Query(default=None, description="Latitude (requires lon)"),
    lon: float | None = Query(default=None, description="Longitude (requires lat)"),
) -> CurrentWeatherResponse:
    has_coords = lat is not None and lon is not None
    has_partial = (lat is None) != (lon is None)
    has_location = location is not None and location.strip()

    if has_partial:
        raise RequestValidationError([{"loc": ["query"], "msg": "Provide both lat and lon, or neither", "type": "value_error"}])
    if not has_coords and not has_location:
        raise RequestValidationError([{"loc": ["query"], "msg": "Provide either 'location' or both 'lat' and 'lon'", "type": "value_error"}])

    return await weather_service.get_current_weather(location, lat, lon)


@router.post("", response_model=WeatherSearchResponse, status_code=201, summary="Save a weather search")
async def create_search(
    payload: WeatherSearchCreate,
    db: Session = Depends(get_db),
) -> WeatherSearchResponse:
    return await weather_service.create_weather_search(payload, db)


@router.get("", response_model=WeatherSearchListResponse, summary="List saved weather searches")
def list_searches(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> WeatherSearchListResponse:
    return weather_service.list_weather_searches(db, limit, offset)


@router.get("/{record_id}", response_model=WeatherSearchResponse, summary="Get a saved search by ID")
def get_search(record_id: int, db: Session = Depends(get_db)) -> WeatherSearchResponse:
    return weather_service.get_weather_search(record_id, db)


@router.put("/{record_id}", response_model=WeatherSearchResponse, summary="Update a saved search")
async def update_search(
    record_id: int,
    payload: WeatherSearchUpdate,
    db: Session = Depends(get_db),
) -> WeatherSearchResponse:
    return await weather_service.update_weather_search(record_id, payload, db)


@router.delete("/{record_id}", status_code=204, summary="Delete a saved search")
def delete_search(record_id: int, db: Session = Depends(get_db)) -> Response:
    weather_service.delete_weather_search(record_id, db)
    return Response(status_code=204)
