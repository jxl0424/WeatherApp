"""Unit tests for Pydantic v2 schemas — no DB or HTTP required."""
from datetime import date, timedelta

import pytest

from app.schemas.weather import WeatherSearchCreate


def make_payload(**kwargs) -> dict:
    today = date.today()
    base = {
        "location_query": "Tokyo",
        "start_date": today,
        "end_date": today + timedelta(days=3),
    }
    base.update(kwargs)
    return base


def test_valid_payload():
    p = WeatherSearchCreate(**make_payload())
    assert p.location_query == "Tokyo"


def test_blank_location_rejected():
    with pytest.raises(Exception, match="blank"):
        WeatherSearchCreate(**make_payload(location_query="   "))


def test_end_before_start_rejected():
    today = date.today()
    with pytest.raises(Exception):
        WeatherSearchCreate(**make_payload(start_date=today, end_date=today - timedelta(days=1)))


def test_range_over_16_days_rejected():
    today = date.today()
    with pytest.raises(Exception, match="16"):
        WeatherSearchCreate(**make_payload(start_date=today, end_date=today + timedelta(days=17)))


def test_location_gets_stripped():
    p = WeatherSearchCreate(**make_payload(location_query="  Paris  "))
    assert p.location_query == "Paris"
