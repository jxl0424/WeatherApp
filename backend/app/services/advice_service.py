from app.integrations.nvidia_client import chat, generate_advice, generate_summary, resolve_location
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


async def get_travel_advice(req: AdviceRequest) -> AdviceResponse:
    return await generate_advice(req)


async def get_weather_summary(req: WeatherSummaryRequest) -> WeatherSummaryResponse:
    return await generate_summary(req)


async def get_resolved_location(req: ResolveLocationRequest) -> ResolveLocationResponse:
    return await resolve_location(req)


async def get_chat_reply(req: ChatRequest) -> ChatResponse:
    return await chat(req)
