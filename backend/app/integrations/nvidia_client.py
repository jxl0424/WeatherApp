"""
NVIDIA NIM client — OpenAI-compatible chat completions.
Falls back gracefully if the API key is missing.
"""

import json

from openai import AsyncOpenAI, APIError

from app.core.config import settings
from app.core.exceptions import AIUnavailableError
from app.schemas.weather import AdviceRequest, AdviceResponse

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


async def generate_advice(req: AdviceRequest) -> AdviceResponse:
    if not settings.NVIDIA_API_KEY:
        raise AIUnavailableError(
            "AI advisor is unavailable — NVIDIA_API_KEY is not configured."
        )

    client = AsyncOpenAI(
        base_url=settings.NVIDIA_BASE_URL,
        api_key=settings.NVIDIA_API_KEY,
    )

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
