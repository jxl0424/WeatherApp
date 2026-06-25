from fastapi import APIRouter

from app.schemas.weather import (
    AdviceRequest,
    AdviceResponse,
    ChatRequest,
    ChatResponse,
    ResolveLocationRequest,
    ResolveLocationResponse,
    WeatherSummaryRequest,
    WeatherSummaryResponse,
)
from app.services.advice_service import (
    get_chat_reply,
    get_resolved_location,
    get_travel_advice,
    get_weather_summary,
)

router = APIRouter(prefix="/advice", tags=["advice"])


@router.post("", response_model=AdviceResponse, summary="AI packing and travel advice")
async def travel_advice(req: AdviceRequest) -> AdviceResponse:
    return await get_travel_advice(req)


@router.post("/summary", response_model=WeatherSummaryResponse, summary="Plain-English weather narrative")
async def weather_summary(req: WeatherSummaryRequest) -> WeatherSummaryResponse:
    return await get_weather_summary(req)


@router.post("/resolve-location", response_model=ResolveLocationResponse, summary="Map a fuzzy query to a concrete city")
async def resolve_location(req: ResolveLocationRequest) -> ResolveLocationResponse:
    return await get_resolved_location(req)


@router.post("/chat", response_model=ChatResponse, summary="Weather-aware Q&A chat")
async def weather_chat(req: ChatRequest) -> ChatResponse:
    return await get_chat_reply(req)
