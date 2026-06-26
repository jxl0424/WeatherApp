import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.weather import (
    AdviceRequest,
    AdviceResponse,
    ResolveLocationRequest,
    ResolveLocationResponse,
    WeatherSummaryRequest,
    WeatherSummaryResponse,
    ChatRequest,
)
from app.services.advice_service import (
    get_chat_reply,
    get_resolved_location,
    get_travel_advice,
    get_weather_summary,
)
from app.services.guardrails import REFUSAL, is_likely_injection

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


@router.post("/chat", summary="Weather-aware Q&A chat")
async def weather_chat(req: ChatRequest) -> StreamingResponse:
    if is_likely_injection(req.message):
        async def _refusal():
            yield f"data: {json.dumps({'token': REFUSAL})}\n\n"
            yield "data: [DONE]\n\n"
        return StreamingResponse(_refusal(), media_type="text/event-stream")

    async def _stream():
        try:
            async for token in get_chat_reply(req):
                yield f"data: {json.dumps({'token': token})}\n\n"
        except Exception:
            pass
        yield "data: [DONE]\n\n"

    return StreamingResponse(_stream(), media_type="text/event-stream")
