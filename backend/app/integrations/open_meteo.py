"""
HTTP client for Open-Meteo APIs.
No API key required — all endpoints are public.

Endpoints used:
  Geocoding : https://geocoding-api.open-meteo.com/v1/search
  Forecast  : https://api.open-meteo.com/v1/forecast
  Air Quality: https://air-quality-api.open-meteo.com/v1/air-quality
"""

from datetime import date

import httpx

from app.core.exceptions import LocationNotFoundError, UpstreamWeatherError
from app.schemas.weather import AQIResponse, CurrentWeather, ForecastDay

# WMO Weather interpretation codes → human-readable strings
WMO_CODES: dict[int, str] = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Icy fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight showers",
    81: "Moderate showers",
    82: "Violent showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail",
}

AQI_LABELS = [
    (0, "Good"),
    (50, "Moderate"),
    (100, "Unhealthy for Sensitive"),
    (150, "Unhealthy"),
    (200, "Very Unhealthy"),
    (300, "Hazardous"),
]


def _aqi_label(aqi: int | None) -> str:
    if aqi is None:
        return "Unknown"
    for threshold, label in reversed(AQI_LABELS):
        if aqi >= threshold:
            return label
    return "Good"


def _wmo(code: int | None) -> str:
    if code is None:
        return "Unknown"
    return WMO_CODES.get(code, f"Code {code}")


async def geocode(location_query: str) -> tuple[float, float, str]:
    """Return (latitude, longitude, resolved_name) or raise LocationNotFoundError."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": location_query, "count": 1, "language": "en", "format": "json"},
            )
            resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise UpstreamWeatherError(f"Geocoding API error: {exc}") from exc

    data = resp.json()
    results = data.get("results")
    if not results:
        raise LocationNotFoundError(f"Location '{location_query}' not found")

    top = results[0]
    parts = [top.get("name"), top.get("admin1"), top.get("country")]
    resolved_name = ", ".join(p for p in parts if p)
    return float(top["latitude"]), float(top["longitude"]), resolved_name


async def get_forecast(
    lat: float,
    lon: float,
    start_date: date | None = None,
    end_date: date | None = None,
) -> tuple[CurrentWeather, list[ForecastDay]]:
    """Fetch current weather + up to 7-day daily forecast."""
    params: dict = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "apparent_temperature",
            "relative_humidity_2m",
            "wind_speed_10m",
            "weather_code",
        ],
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "weather_code",
            "precipitation_sum",
            "wind_speed_10m_max",
        ],
        "timezone": "auto",
        "forecast_days": 7,
    }
    if start_date:
        params["start_date"] = start_date.isoformat()
    if end_date:
        params["end_date"] = end_date.isoformat()

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get("https://api.open-meteo.com/v1/forecast", params=params)
            resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise UpstreamWeatherError(f"Weather API error: {exc}") from exc

    try:
        data = resp.json()
        cur = data.get("current", {})
        daily = data.get("daily", {})

        current = CurrentWeather(
            temperature=cur.get("temperature_2m", 0),
            feels_like=cur.get("apparent_temperature"),
            humidity=cur.get("relative_humidity_2m"),
            wind_speed=cur.get("wind_speed_10m"),
            condition=_wmo(cur.get("weather_code")),
            condition_code=cur.get("weather_code", 0),
        )

        forecast: list[ForecastDay] = []
        dates = daily.get("time", [])
        for i, d in enumerate(dates):
            forecast.append(
                ForecastDay(
                    date=d,
                    temp_min=daily["temperature_2m_min"][i],
                    temp_max=daily["temperature_2m_max"][i],
                    condition=_wmo(daily["weather_code"][i]),
                    condition_code=daily["weather_code"][i],
                    precipitation_sum=daily.get("precipitation_sum", [None] * (i + 1))[i],
                    wind_speed_max=daily.get("wind_speed_10m_max", [None] * (i + 1))[i],
                )
            )
    except (KeyError, IndexError, TypeError) as exc:
        raise UpstreamWeatherError(f"Unexpected forecast response format: {exc}") from exc

    return current, forecast


async def get_aqi(lat: float, lon: float) -> AQIResponse:
    """Fetch current Air Quality Index from Open-Meteo."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                "https://air-quality-api.open-meteo.com/v1/air-quality",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": ["us_aqi", "pm2_5", "pm10"],
                },
            )
            resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise UpstreamWeatherError(f"Air quality API error: {exc}") from exc

    data = resp.json()
    cur = data.get("current", {})
    aqi_val = cur.get("us_aqi")

    return AQIResponse(
        aqi=aqi_val,
        label=_aqi_label(aqi_val),
        pm2_5=cur.get("pm2_5"),
        pm10=cur.get("pm10"),
    )
