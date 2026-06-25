"""
NVIDIA NIM client — OpenAI-compatible chat completions.
Falls back gracefully if the API key is missing.
"""

import json

from openai import AsyncOpenAI, APIError

from app.core.config import settings
from app.core.exceptions import AIUnavailableError
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

_SYSTEM_PROMPT = """You are an expert travel weather advisor. Given current weather conditions and a forecast, respond ONLY with a JSON object (no markdown, no explanation) matching this exact structure:
{
  "clothing": [],
  "packing": [],
  "activities": [],
  "travel_considerations": [],
  "warnings": []
}
Each list should contain 2-5 concise, practical, specific strings. The "warnings" list should only contain items when there is a genuine safety or health concern (empty list is fine)."""


def _build_prompt(req: AdviceRequest) -> str:
    forecast_lines = "\n".join(
        f"  {f.date}: {f.condition}, {f.temp_min}–{f.temp_max}°C, "
        f"precip {f.precipitation_sum or 0}mm"
        for f in req.forecast[:5]
    )
    aqi_note = ""
    if req.current.aqi is not None:
        aqi_note = f"\nAir Quality: AQI {req.current.aqi} ({req.current.aqi_label})"

    return (
        f"Location: {req.location}\n"
        f"Current: {req.current.condition}, {req.current.temperature}°C "
        f"(feels like {req.current.feels_like}°C), "
        f"humidity {req.current.humidity}%, wind {req.current.wind_speed} km/h"
        f"{aqi_note}\n"
        f"5-day forecast:\n{forecast_lines}"
    )


def _require_key() -> str:
    if not settings.NVIDIA_API_KEY:
        raise AIUnavailableError("AI advisor is unavailable — NVIDIA_API_KEY is not configured.")
    return settings.NVIDIA_API_KEY


def _client() -> AsyncOpenAI:
    return AsyncOpenAI(base_url=settings.NVIDIA_BASE_URL, api_key=_require_key())


async def generate_advice(req: AdviceRequest) -> AdviceResponse:
    client = _client()
    try:
        response = await client.chat.completions.create(
            model=settings.NVIDIA_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": _build_prompt(req)},
            ],
            temperature=0.4,
            max_tokens=600,
        )
    except APIError as exc:
        raise AIUnavailableError(f"NVIDIA NIM error: {exc}") from exc

    raw = response.choices[0].message.content or "{}"
    try:
        parsed = json.loads(raw)
        return AdviceResponse(**parsed)
    except (json.JSONDecodeError, ValueError):
        return AdviceResponse(
            travel_considerations=["AI response could not be parsed. Please try again."]
        )


_SUMMARY_SYSTEM = (
    "You are a travel weather narrator. Given weather data, write 2–3 vivid, concise sentences "
    "describing what the weather actually feels like and what a traveller should expect. "
    "No headings, no bullet points, no markdown — just flowing prose."
)


async def generate_summary(req: WeatherSummaryRequest) -> WeatherSummaryResponse:
    client = _client()
    forecast_lines = "\n".join(
        f"  {f.date}: {f.condition}, {f.temp_min}–{f.temp_max}°C"
        for f in req.forecast[:5]
    )
    user_msg = (
        f"Location: {req.location}\n"
        f"Right now: {req.current.condition}, {req.current.temperature}°C "
        f"(feels like {req.current.feels_like}°C), humidity {req.current.humidity}%\n"
        f"Coming days:\n{forecast_lines}"
    )
    try:
        response = await client.chat.completions.create(
            model=settings.NVIDIA_MODEL,
            messages=[
                {"role": "system", "content": _SUMMARY_SYSTEM},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.6,
            max_tokens=180,
        )
    except APIError as exc:
        raise AIUnavailableError(f"NVIDIA NIM error: {exc}") from exc

    summary = (response.choices[0].message.content or "").strip()
    return WeatherSummaryResponse(summary=summary)


_RESOLVE_SYSTEM = (
    "You map fuzzy or descriptive travel queries to ONE specific, real city. "
    "Respond ONLY with a JSON object (no markdown) with this exact shape: "
    '{"suggested_location": "<City, Country>", "reasoning": "<one sentence>"}'
)


async def resolve_location(req: ResolveLocationRequest) -> ResolveLocationResponse:
    client = _client()
    try:
        response = await client.chat.completions.create(
            model=settings.NVIDIA_MODEL,
            messages=[
                {"role": "system", "content": _RESOLVE_SYSTEM},
                {"role": "user", "content": req.query},
            ],
            temperature=0.3,
            max_tokens=120,
        )
    except APIError as exc:
        raise AIUnavailableError(f"NVIDIA NIM error: {exc}") from exc

    raw = (response.choices[0].message.content or "{}").strip()
    try:
        parsed = json.loads(raw)
        return ResolveLocationResponse(
            suggested_location=parsed["suggested_location"],
            reasoning=parsed.get("reasoning", ""),
        )
    except (json.JSONDecodeError, KeyError, ValueError):
        return ResolveLocationResponse(
            suggested_location=req.query,
            reasoning="AI could not parse the location; using your query directly.",
        )


def _chat_system(req: ChatRequest) -> str:
    forecast_lines = "\n".join(
        f"  {f.date}: {f.condition}, {f.temp_min}–{f.temp_max}°C, "
        f"precip {f.precipitation_sum or 0}mm"
        for f in req.forecast[:5]
    )
    aqi_note = ""
    if req.current.aqi is not None:
        aqi_note = f"\nAir Quality: AQI {req.current.aqi} ({req.current.aqi_label})"
    return (
        "You are a helpful weather and travel assistant. Answer the user's questions "
        "about the weather conditions below. Be concise and practical.\n\n"
        f"Location: {req.location}\n"
        f"Current: {req.current.condition}, {req.current.temperature}°C "
        f"(feels like {req.current.feels_like}°C), "
        f"humidity {req.current.humidity}%, wind {req.current.wind_speed} km/h"
        f"{aqi_note}\n"
        f"5-day forecast:\n{forecast_lines}"
    )


async def chat(req: ChatRequest) -> ChatResponse:
    client = _client()
    messages: list[dict] = [{"role": "system", "content": _chat_system(req)}]
    for msg in req.history:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": req.message})

    try:
        response = await client.chat.completions.create(
            model=settings.NVIDIA_MODEL,
            messages=messages,
            temperature=0.5,
            max_tokens=400,
        )
    except APIError as exc:
        raise AIUnavailableError(f"NVIDIA NIM error: {exc}") from exc

    reply = (response.choices[0].message.content or "").strip()
    return ChatResponse(reply=reply)
