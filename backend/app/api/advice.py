from fastapi import APIRouter

from app.schemas.weather import AdviceRequest, AdviceResponse
from app.services.advice_service import get_travel_advice

router = APIRouter(prefix="/advice", tags=["advice"])


@router.post("", response_model=AdviceResponse)
async def travel_advice(req: AdviceRequest) -> AdviceResponse:
    return await get_travel_advice(req)
