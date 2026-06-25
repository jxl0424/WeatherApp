"""Tests for the NVIDIA NIM advice integration — all HTTP calls mocked."""
import json
from datetime import date
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from openai import APIError

from app.core.exceptions import AIUnavailableError
from app.integrations.nvidia_client import generate_advice
from app.schemas.weather import AdviceRequest, CurrentWeather, ForecastDay

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
