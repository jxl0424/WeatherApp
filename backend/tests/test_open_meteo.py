"""Tests for Open-Meteo integration helpers — mocks HTTP, no real calls."""
import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock, patch

from app.core.exceptions import LocationNotFoundError, UpstreamWeatherError
from app.integrations.open_meteo import geocode


def _mock_client(response: MagicMock) -> MagicMock:
    """Build a mock httpx.AsyncClient context manager that returns `response` from .get()."""
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=response)

    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=mock_client)
    cm.__aexit__ = AsyncMock(return_value=False)
    return cm


def _geo_response(results: list) -> MagicMock:
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json.return_value = {"results": results}
    return resp


@pytest.mark.asyncio
async def test_geocode_not_found():
    with patch("app.integrations.open_meteo.httpx.AsyncClient", return_value=_mock_client(_geo_response([]))):
        with pytest.raises(LocationNotFoundError):
            await geocode("xyznotaplace123")


@pytest.mark.asyncio
async def test_geocode_upstream_error():
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=httpx.ConnectError("timeout"))
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=mock_client)
    cm.__aexit__ = AsyncMock(return_value=False)

    with patch("app.integrations.open_meteo.httpx.AsyncClient", return_value=cm):
        with pytest.raises(UpstreamWeatherError):
            await geocode("Paris")


@pytest.mark.asyncio
async def test_geocode_returns_coords():
    results = [{"latitude": 48.853, "longitude": 2.349, "name": "Paris", "admin1": "Île-de-France", "country": "France"}]
    with patch("app.integrations.open_meteo.httpx.AsyncClient", return_value=_mock_client(_geo_response(results))):
        lat, lon, name = await geocode("Paris")
        assert lat == 48.853
        assert "Paris" in name
