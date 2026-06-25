"""Tests for the NVIDIA NIM advice integration — all HTTP calls mocked."""
import json
from datetime import date
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from openai import APIError

from app.core.exceptions import AIUnavailableError
from app.integrations.nvidia_client import chat, generate_advice, generate_summary, resolve_location
from app.schemas.weather import (
    AdviceRequest,
    ChatMessage,
    ChatRequest,
    CurrentWeather,
    ForecastDay,
    ResolveLocationRequest,
    WeatherSummaryRequest,
)

_LOCATION = "Tokyo, Japan"

_CURRENT = CurrentWeather(
    temperature=22.0,
    feels_like=21.0,
    humidity=60,
    wind_speed=12.0,
    condition="Partly cloudy",
    condition_code=2,
    aqi=35,
    aqi_label="Good",
)

_FORECAST = [
    ForecastDay(
        date=date(2026, 6, 25),
        temp_min=18.0,
        temp_max=26.0,
        condition="Partly cloudy",
        condition_code=2,
    )
]

_REQUEST = AdviceRequest(location=_LOCATION, current=_CURRENT, forecast=_FORECAST)

_VALID_PAYLOAD = json.dumps({
    "clothing": ["Light layers"],
    "packing": ["Umbrella"],
    "activities": ["Sightseeing"],
    "travel_considerations": ["Book in advance"],
    "warnings": [],
})


def _make_response(content: str) -> MagicMock:
    msg = MagicMock()
    msg.content = content
    choice = MagicMock()
    choice.message = msg
    resp = MagicMock()
    resp.choices = [choice]
    return resp


@pytest.mark.asyncio
async def test_missing_api_key_raises():
    with patch("app.integrations.nvidia_client.settings") as mock_settings:
        mock_settings.NVIDIA_API_KEY = ""
        with pytest.raises(AIUnavailableError, match="NVIDIA_API_KEY"):
            await generate_advice(_REQUEST)


@pytest.mark.asyncio
async def test_valid_response_parsed():
    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(return_value=_make_response(_VALID_PAYLOAD))
    with patch("app.integrations.nvidia_client.AsyncOpenAI", return_value=mock_client):
        result = await generate_advice(_REQUEST)
    assert result.clothing == ["Light layers"]
    assert result.warnings == []


@pytest.mark.asyncio
async def test_malformed_json_returns_fallback():
    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(return_value=_make_response("not json {{{"))
    with patch("app.integrations.nvidia_client.AsyncOpenAI", return_value=mock_client):
        result = await generate_advice(_REQUEST)
    assert result.travel_considerations == ["AI response could not be parsed. Please try again."]


@pytest.mark.asyncio
async def test_api_error_raises():
    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=APIError("rate limited", request=MagicMock(spec=httpx.Request), body=None)
    )
    with patch("app.integrations.nvidia_client.AsyncOpenAI", return_value=mock_client):
        with pytest.raises(AIUnavailableError, match="NVIDIA NIM"):
            await generate_advice(_REQUEST)


# ── Summary tests ─────────────────────────────────────────────────────────────

_SUMMARY_REQ = WeatherSummaryRequest(location=_LOCATION, current=_CURRENT, forecast=_FORECAST)


@pytest.mark.asyncio
async def test_summary_missing_key_raises():
    with patch("app.integrations.nvidia_client.settings") as mock_settings:
        mock_settings.NVIDIA_API_KEY = ""
        with pytest.raises(AIUnavailableError, match="NVIDIA_API_KEY"):
            await generate_summary(_SUMMARY_REQ)


@pytest.mark.asyncio
async def test_summary_returns_text():
    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(
        return_value=_make_response("Tokyo is warm and humid today with pleasant breezes.")
    )
    with patch("app.integrations.nvidia_client.AsyncOpenAI", return_value=mock_client):
        result = await generate_summary(_SUMMARY_REQ)
    assert "Tokyo" in result.summary


@pytest.mark.asyncio
async def test_summary_api_error_raises():
    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=APIError("timeout", request=MagicMock(spec=httpx.Request), body=None)
    )
    with patch("app.integrations.nvidia_client.AsyncOpenAI", return_value=mock_client):
        with pytest.raises(AIUnavailableError):
            await generate_summary(_SUMMARY_REQ)


# ── Resolve location tests ────────────────────────────────────────────────────

_RESOLVE_REQ = ResolveLocationRequest(query="somewhere warm in Europe next week")
_RESOLVE_PAYLOAD = json.dumps({"suggested_location": "Lisbon, Portugal", "reasoning": "Lisbon has warm sunny weather in summer."})


@pytest.mark.asyncio
async def test_resolve_missing_key_raises():
    with patch("app.integrations.nvidia_client.settings") as mock_settings:
        mock_settings.NVIDIA_API_KEY = ""
        with pytest.raises(AIUnavailableError):
            await resolve_location(_RESOLVE_REQ)


@pytest.mark.asyncio
async def test_resolve_returns_city():
    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(return_value=_make_response(_RESOLVE_PAYLOAD))
    with patch("app.integrations.nvidia_client.AsyncOpenAI", return_value=mock_client):
        result = await resolve_location(_RESOLVE_REQ)
    assert result.suggested_location == "Lisbon, Portugal"
    assert result.reasoning


@pytest.mark.asyncio
async def test_resolve_malformed_falls_back_to_query():
    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(return_value=_make_response("not json"))
    with patch("app.integrations.nvidia_client.AsyncOpenAI", return_value=mock_client):
        result = await resolve_location(_RESOLVE_REQ)
    assert result.suggested_location == _RESOLVE_REQ.query


# ── Chat tests ────────────────────────────────────────────────────────────────

_CHAT_REQ = ChatRequest(
    location=_LOCATION,
    current=_CURRENT,
    forecast=_FORECAST,
    history=[ChatMessage(role="user", content="Hello"), ChatMessage(role="assistant", content="Hi!")],
    message="Is Wednesday good for hiking?",
)


@pytest.mark.asyncio
async def test_chat_missing_key_raises():
    with patch("app.integrations.nvidia_client.settings") as mock_settings:
        mock_settings.NVIDIA_API_KEY = ""
        with pytest.raises(AIUnavailableError):
            await chat(_CHAT_REQ)


@pytest.mark.asyncio
async def test_chat_returns_reply():
    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(
        return_value=_make_response("Wednesday looks great for hiking — partly cloudy and mild.")
    )
    with patch("app.integrations.nvidia_client.AsyncOpenAI", return_value=mock_client):
        result = await chat(_CHAT_REQ)
    assert "Wednesday" in result.reply


@pytest.mark.asyncio
async def test_chat_api_error_raises():
    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=APIError("error", request=MagicMock(spec=httpx.Request), body=None)
    )
    with patch("app.integrations.nvidia_client.AsyncOpenAI", return_value=mock_client):
        with pytest.raises(AIUnavailableError):
            await chat(_CHAT_REQ)
