# Database Design

**Engine**: PostgreSQL 16  
**ORM**: SQLAlchemy 2.0  
**Migrations**: Alembic  

---

## Table: `weather_searches`

| Column | Postgres Type | Constraints | Notes |
|---|---|---|---|
| `id` | `BIGSERIAL` | PRIMARY KEY | Auto-increment |
| `location_query` | `VARCHAR(255)` | NOT NULL | Raw user input (e.g. "Paris", "94103") |
| `resolved_location_name` | `VARCHAR(255)` | NOT NULL | Canonical geocoder output (e.g. "Paris, Île-de-France, France") |
| `latitude` | `NUMERIC(8,5)` | NOT NULL | Decimal degrees; validated –90 ≤ x ≤ 90 at app layer |
| `longitude` | `NUMERIC(8,5)` | NOT NULL | Decimal degrees; validated –180 ≤ x ≤ 180 at app layer |
| `start_date` | `DATE` | NOT NULL | User-specified range start |
| `end_date` | `DATE` | NOT NULL, CHECK (`end_date >= start_date`) | User-specified range end; max 16 days after start |
| `weather_condition` | `VARCHAR(64)` | NOT NULL | Human-readable WMO condition code label |
| `temperature` | `NUMERIC(5,2)` | NOT NULL | °C; current temp at time of first fetch |
| `humidity` | `SMALLINT` | CHECK (0 ≤ humidity ≤ 100) | % relative humidity; nullable |
| `wind_speed` | `NUMERIC(5,2)` | | km/h; nullable |
| `created_at` | `TIMESTAMPTZ` | NOT NULL DEFAULT `now()` | Set on INSERT |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL DEFAULT `now()` | Refreshed on every UPDATE via SQLAlchemy `onupdate` |

---

## Indexes

| Index | Columns | Purpose |
|---|---|---|
| PK | `id` | Row lookup by ID |
| `ix_weather_searches_created_at` | `created_at DESC` | Chronological list ordering |
| `ix_weather_searches_resolved_location_name` | `resolved_location_name` | Future filter-by-location |

---

## SQLAlchemy Model

```python
class WeatherSearch(Base):
    __tablename__ = "weather_searches"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    location_query: Mapped[str] = mapped_column(String(255), nullable=False)
    resolved_location_name: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[Decimal] = mapped_column(Numeric(8, 5), nullable=False)
    longitude: Mapped[Decimal] = mapped_column(Numeric(8, 5), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    weather_condition: Mapped[str] = mapped_column(String(64), nullable=False)
    temperature: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    humidity: Mapped[Optional[int]] = mapped_column(SmallInteger)
    wind_speed: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(),
        onupdate=func.now(), nullable=False
    )
```

---

## Validation Rules (enforced in Pydantic schemas)

| Field | Rule |
|---|---|
| `location_query` | 1–255 chars, non-blank after strip |
| `start_date` | Valid date; not more than 2 years in the past |
| `end_date` | >= `start_date`; <= `start_date + 16 days` |
| `latitude` | –90.0 ≤ value ≤ 90.0 |
| `longitude` | –180.0 ≤ value ≤ 180.0 |
| `humidity` | 0–100 if provided |

Location existence is validated via Open-Meteo Geocoding API at service layer (not the DB layer).

---

## Migration Strategy

- `alembic init alembic` → generates `alembic/` directory and `alembic.ini`
- `alembic revision --autogenerate -m "create_weather_searches"` → generates initial migration
- `alembic upgrade head` → applies migration
- Each subsequent schema change gets its own numbered revision
