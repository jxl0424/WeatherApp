from fastapi import APIRouter, Query

from app.integrations.open_meteo import get_aqi
from app.schemas.weather import AQIResponse

router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.get("/aqi", response_model=AQIResponse)
async def air_quality(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
) -> AQIResponse:
    return await get_aqi(lat, lon)
