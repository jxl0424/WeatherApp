from datetime import date, timedelta


def clamp_forecast_end(start: date, end: date) -> date:
    """Return end_date clamped to Open-Meteo's 16-day forecast horizon."""
    max_end = start + timedelta(days=16)
    return min(end, max_end)
