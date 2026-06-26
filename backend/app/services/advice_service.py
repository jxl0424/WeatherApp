from typing import AsyncGenerator

from app.integrations.nvidia_client import chat, generate_advice, generate_summary, resolve_location
from app.schemas.weather import (
    AdviceRequest,
    AdviceResponse,
    ChatRequest,
    ResolveLocationRequest,
    ResolveLocationResponse,
    WeatherSummaryRequest,
    WeatherSummaryResponse,
)
from app.services import ai_cache


async def get_travel_advice(req: AdviceRequest) -> AdviceResponse:
    cached = ai_cache.get_advice(req.location, req.current.condition, req.current.temperature)
    if cached is not None:
        return cached
    result = await generate_advice(req)
    ai_cache.set_advice(req.location, req.current.condition, req.current.temperature, result)
    return result


async def get_weather_summary(req: WeatherSummaryRequest) -> WeatherSummaryResponse:
    cached = ai_cache.get_summary(req.location, req.current.condition, req.current.temperature)
    if cached is not None:
        return cached
    result = await generate_summary(req)
    ai_cache.set_summary(req.location, req.current.condition, req.current.temperature, result)
    return result


async def get_resolved_location(req: ResolveLocationRequest) -> ResolveLocationResponse:
    return await resolve_location(req)


async def get_chat_reply(req: ChatRequest) -> AsyncGenerator[str, None]:
    async for token in chat(req):
        yield token
