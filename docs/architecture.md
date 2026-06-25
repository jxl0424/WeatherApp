# Architecture

## System Topology

```
┌─────────────────────────────────────────────────────────────────┐
│                          Browser                                │
│                                                                 │
│   Next.js 15 (port 3000)                                        │
│   ├── App Router pages                                          │
│   ├── TanStack Query (fetch + cache + error states)             │
│   └── shadcn/ui + Tailwind                                      │
└────────────────────┬────────────────────────────────────────────┘
                     │ REST (JSON) over HTTP
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│   FastAPI (port 8000)                                           │
│                                                                 │
│   api/                                                          │
│   ├── weather.py    CRUD + ad-hoc weather routes                │
│   ├── advice.py     AI routes (advisor, summary, chat, resolve) │
│   └── export.py     CSV / JSON / Markdown export                │
│                                                                 │
│   services/         Business logic (called by routes)           │
│   integrations/     External HTTP clients                       │
│   ├── open_meteo.py → Open-Meteo Weather + Geocoding + AQI     │
│   └── nvidia_client.py → NVIDIA NIM (4 inference functions)    │
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
User types "Tokyo" (or "warm beach in Europe" → AI resolves first)
    │
    ▼
Frontend: GET /api/v1/weather/current?location=Tokyo
    │
    ▼
FastAPI: WeatherService.get_current(location="Tokyo")
    │
    ├─► open_meteo.geocode("Tokyo") → {lat, lon, name}
    ├─► asyncio.gather(
    │     open_meteo.get_forecast(lat, lon),   ─┐ concurrent
    │     open_meteo.get_aqi(lat, lon)          ─┘
    │   )
    │
    ▼
Response: CurrentWeatherResponse (NOT persisted)
    │
    ▼
Frontend: renders weather card + AI narrative summary (auto-fetch)
          + 5-day forecast + AI advisor button + chat panel
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

## Data Flow: AI Features (four endpoints, same NIM backend)

```
POST /advice/summary          (auto-triggered after weather loads)
POST /advice                  (user clicks "Get Travel Advice")
POST /advice/resolve-location (user clicks Sparkles button with NL query)
POST /advice/chat             (user sends a message in the chat panel)
    │
    ▼
FastAPI: advice_service → nvidia_client.<function>(req)
    │
    ├─► Builds system prompt embedding weather context
    ├─► AsyncOpenAI.chat.completions.create(model=NIM_MODEL, ...)
    └─► Parses plain-text or JSON response into typed Pydantic model
    │
    ▼
Response varies by endpoint:
  /summary          → { summary: str }
  /advice           → { clothing, packing, activities, travel_considerations, warnings }
  /resolve-location → { suggested_location: str, reasoning: str }
  /chat             → { reply: str }
    │
    ▼
Frontend: renders summary inline, advice panel, fills search input, or appends chat bubble
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
