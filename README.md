# AI-Powered Weather Travel Advisor

**Submitted by:** Brendan Lee  
**Assessment completed:** Full Stack (Tech Assessment #1 + #2)

## Project Overview

Instead of just displaying raw weather data, this app helps users make **smart travel decisions** based on current conditions, 5-day forecasts, and AI-generated advice — answering the question *"What should a traveler consider that isn't obvious from a temperature number?"*

**Key capabilities:**
- Search weather by city, zip code, GPS coordinates, landmark, or natural-language description
- Use your browser's current location
- View current weather conditions with icons and Air Quality Index
- View a 5-day forecast
- AI-generated plain-English weather narrative (auto-loads with every search)
- AI travel advisor — clothing, packing, activities, and safety warnings
- Natural-language location search — type "warm beach in Europe" and AI picks a city
- Weather chat — ask freeform questions like "Is Wednesday good for hiking?" with full conversation history
- Save weather searches (CRUD) with date range support
- Export saved searches to CSV, JSON, or Markdown

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query |
| Backend | FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, Uvicorn |
| Database | PostgreSQL 16 |
| Weather | Open-Meteo (weather, geocoding, air quality) — no API key required |
| AI | NVIDIA NIM (minimax-m3 via OpenAI-compatible API) |
| Deploy | Docker + Docker Compose |

---

## Quick Start (Docker)

```bash
# 1. Clone
git clone https://github.com/jxl0424/WeatherApp.git
cd WeatherApp

# 2. Configure environment
cp .env.example .env
# Edit .env and add your NVIDIA_API_KEY (required for AI advisor only)

# 3. Start all services
docker compose up --build

# 4. Open in browser
#    App:     http://localhost:3000
#    API docs: http://localhost:8000/docs
```

> **Note:** All weather features work without any API key. The four AI features (narrative summary, travel advisor, natural-language location search, and weather chat) require `NVIDIA_API_KEY`. If the key is absent they show a graceful "unavailable" message instead of crashing.

---

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements/dev.txt

# Run Postgres locally (or use Docker for just the DB)
docker compose up db -d

# Apply migrations
alembic upgrade head

# Start dev server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# Opens at http://localhost:3000
```

---

## Environment Variables

| Variable | Required | Default | Notes |
|---|---|---|---|
| `DATABASE_URL` | Yes | — | PostgreSQL connection string |
| `NVIDIA_API_KEY` | For AI only | — | From https://build.nvidia.com |
| `NVIDIA_BASE_URL` | No | `https://integrate.api.nvidia.com/v1` | |
| `NVIDIA_MODEL` | No | `minimaxai/minimax-m3` | Any NIM-compatible model |
| `ALLOWED_ORIGINS` | No | `http://localhost:3000` | CORS allowed origins |
| `APP_ENV` | No | `development` | Runtime environment label |

---

## API Documentation

Full REST API contract: [docs/api-design.md](docs/api-design.md)  
Interactive Swagger UI: `http://localhost:8000/docs` (when backend is running)

---

## Architecture

See [docs/architecture.md](docs/architecture.md) for the full system diagram and data flow.

---

## Running Tests

```bash
# Backend (21 tests)
cd backend
pytest

# Frontend (5 tests)
cd frontend
npm test
```
