import csv
import io
import json
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.weather_search import WeatherSearch


def _rows(db: Session) -> list[WeatherSearch]:
    return list(db.scalars(select(WeatherSearch).order_by(WeatherSearch.created_at.desc())).all())


def _serialise(value: object) -> str:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    return str(value) if value is not None else ""


HEADERS = [
    "id", "location_query", "resolved_location_name", "latitude", "longitude",
    "start_date", "end_date", "weather_condition", "temperature",
    "humidity", "wind_speed", "created_at", "updated_at",
]


def export_csv(db: Session) -> str:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=HEADERS)
    writer.writeheader()
    for row in _rows(db):
        writer.writerow({h: _serialise(getattr(row, h)) for h in HEADERS})
    return buf.getvalue()


def export_json(db: Session) -> str:
    records = [
        {h: _serialise(getattr(row, h)) for h in HEADERS}
        for row in _rows(db)
    ]
    return json.dumps(records, indent=2)


def export_markdown(db: Session) -> str:
    rows = _rows(db)
    if not rows:
        return "# Weather Searches\n\nNo records found.\n"

    lines = ["# Weather Searches\n"]
    col_widths = {h: max(len(h), max((len(_serialise(getattr(r, h))) for r in rows), default=0)) for h in HEADERS}

    header_line = "| " + " | ".join(h.ljust(col_widths[h]) for h in HEADERS) + " |"
    sep_line = "| " + " | ".join("-" * col_widths[h] for h in HEADERS) + " |"
    lines.append(header_line)
    lines.append(sep_line)
    for row in rows:
        lines.append("| " + " | ".join(_serialise(getattr(row, h)).ljust(col_widths[h]) for h in HEADERS) + " |")

    return "\n".join(lines) + "\n"
