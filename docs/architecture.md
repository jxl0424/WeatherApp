# Architecture

## System Topology

```
┌─────────────────────────────────────────────────────────────────┐
│                          Browser                                │
│                                                                 │
│   Next.js 15 (port 3000)                                        │
│   ├── App Router pages                                          │
│   ├── TanStack Query (fetch + cache + error states)             │
│   ├── shadcn/ui + Tailwind                                      │
│   └── AboutBanner (candidate name + PM Accelerator description) │
└────────────────────┬────────────────────────────────────────────┘
                     │ REST (JSON) over HTTP
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│   FastAPI (port 8000)                                           │
│                                                                 │
│   api/                                                          │
│   ├── weather.py    CRUD routes                                 │
│   ├── advice.py     AI travel advisor route                     │
│   └── export.py     CSV / JSON / Markdown export                │
│                                                                 │
│   services/         Business logic (called by routes)           │
│   integrations/     External HTTP clients                       │
│   └── open_meteo.py → Open-Meteo Weather + Geocoding + AQI     │
│   └── nvidia_client.py → NVIDIA NIM (LLM inference)            │
│                                                                 │
│   models / schemas / db                                         │
└──────────┬───────────────────────────────────────────┬──────────┘
           │ SQLAlchemy 2.0 (psycopg driver)            │ httpx
           ▼                                            ▼
┌──────────────────┐                     ┌──────────────────────────┐
│  PostgreSQL 16   │                     │  External APIs           │
│  (port 5432)     │                     │                          │
│                  │                     │  api.open-meteo.com      │
│  weather_        │                     │  ├─ /v1/search (geo)     │
│  searches table  │                     │  ├─ /v1/forecast (wx)    │
│                  │                     │  └─ /v1/air-quality      │
│                  │                     │                          │
│                  │                     │  integrate.api.nvidia.com│
│                  │                     │  └─ /v1/chat/completions │
└──────────────────┘                     └──────────────────────────┘
```

---

## Data Flow: Ad-hoc Weather Lookup

```
User types "Tokyo"
    │
    ▼
Frontend: POST /api/v1/weather/current?location=Tokyo
    │
    ▼
FastAPI: WeatherService.get_current(location="Tokyo")
    │
    ├─► open_meteo.geocode("Tokyo") → {lat, lon, name}
    ├─► open_meteo.get_forecast(lat, lon) → {current, forecast[]}
    └─► open_meteo.get_aqi(lat, lon) → {aqi, label}
    │
    ▼
Response: CurrentWeatherResponse (NOT persisted)
    │
    ▼
Frontend: renders weather card + 5-day forecast grid
```

---

## Data Flow: Saved Search (CRUD)

```
User fills form: location="Paris", dates=2026-07-01/05
    │
    ▼
Frontend: POST /api/v1/weather
    │
    ▼
FastAPI: WeatherService.create(WeatherSearchCreate)
    │
    ├─► Pydantic v2 validates dates and input length
    ├─► open_meteo.geocode("Paris") → resolves location or raises LocationNotFoundError
    ├─► open_meteo.get_forecast(lat, lon, start_date) → weather snapshot
    └─► db.add(WeatherSearch) → persists row
    │
    ▼
Response: WeatherSearchResponse (201)
    │
    ▼
Frontend: invalidates list query → history table refreshes
```

---

## Data Flow: AI Travel Advice

```
User clicks "Get AI Travel Advice" on a weather card
    │
    ▼
Frontend: POST /api/v1/advice (sends current + forecast + aqi)
    │
    ▼
FastAPI: AdviceService.generate(AdviceRequest)
    │
    ├─► Builds structured prompt from weather data
    ├─► nvidia_client.chat(prompt) → JSON string
    └─► Pydantic v2 parses response into AdviceResponse
    │
    ▼
Response: { clothing, packing, activities, travel_considerations, warnings }
    │
    ▼
Frontend: renders advice panel with categorized cards
```

---

## Deployment (Phase 14)

Three Docker Compose services:

| Service | Image | Port |
|---|---|---|
| `db` | `postgres:16-alpine` | 5432 |
| `backend` | `./backend/Dockerfile` | 8000 |
| `frontend` | `./frontend/Dockerfile` | 3000 |

Startup order: `db` → `backend` (health-check waits for Postgres) → `frontend`.

Alembic migrations run automatically in the backend container's entrypoint before Uvicorn starts.
