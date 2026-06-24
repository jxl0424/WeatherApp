# AI-Powered Weather Travel Advisor

**Submitted by: Brendan Lee**  
Full-Stack submission for the PM Accelerator AI Engineer Intern Technical Assessment (Tech Assessment #1 + #2)

---

## About PM Accelerator

**Product Manager Accelerator (PMA)** is a world-class product management program that helps aspiring and current product managers land their dream PM roles, advance their careers, and build meaningful connections within a global community of product leaders. Through structured mentorship, real-world project experience, and expert-led training, PMA equips professionals with the skills, frameworks, and network needed to thrive in the modern product landscape.

🔗 [LinkedIn: Product Manager Accelerator](https://www.linkedin.com/company/product-manager-accelerator/)

---

## Project Overview

Instead of just displaying raw weather data, this app helps users make **smart travel decisions** based on current conditions, 5-day forecasts, and AI-generated advice — answering the question *"What should a traveler consider that isn't obvious from a temperature number?"*

**Key capabilities:**
- Search weather by city, zip code, GPS coordinates, or landmark
- Use your browser's current location
- View current weather conditions with icons
- View a 5-day forecast
- Save weather searches (CRUD) with date range support
- Export saved searches to CSV, JSON, or Markdown
- Get AI-powered travel recommendations (clothing, packing, activities, warnings)
- See Air Quality Index alongside weather data

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query |
| Backend | FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, Uvicorn |
| Database | PostgreSQL 16 |
| Weather | Open-Meteo (weather, geocoding, air quality) — no API key required |
| AI | NVIDIA NIM (llama-3.1-8b-instruct via OpenAI-compatible API) |
| Deploy | Docker + Docker Compose |

---

## Quick Start (Docker)

```bash
# 1. Clone
git clone <repo-url>
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

> **Note:** All weather features work without any API key. Only the AI Travel Advisor requires `NVIDIA_API_KEY`. If the key is absent, the advisor shows a graceful "unavailable" message instead of crashing.

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
| `NVIDIA_MODEL` | No | `meta/llama-3.1-8b-instruct` | Any NIM-compatible model |
| `ALLOWED_ORIGINS` | No | `http://localhost:3000` | CORS allowed origins |

---

## API Documentation

Full REST API contract: [docs/api-design.md](docs/api-design.md)  
Interactive Swagger UI: `http://localhost:8000/docs` (when backend is running)

---

## Assessment Requirements Checklist

### Tech Assessment #1 (Frontend)
- [x] Location search (city, zip, GPS, landmark)
- [x] Current location via browser geolocation
- [x] Current weather display with icons
- [x] 5-day forecast
- [x] Error handling (location not found, API failures)
- [x] Responsive design (desktop, tablet, mobile)
- [x] Multiple API integrations

### Tech Assessment #2 (Backend)
- [x] CREATE — save weather search with date range + validation
- [x] READ — list and detail views of saved searches
- [x] UPDATE — edit location/dates with re-fetch
- [x] DELETE — remove saved searches
- [x] Location validation via geocoding (fuzzy match)
- [x] Date range validation
- [x] RESTful API with proper HTTP semantics
- [x] Data export (CSV, JSON, Markdown)
- [x] Additional API integration (Open-Meteo Air Quality)

### General
- [x] Candidate name displayed in app: **Brendan Lee**
- [x] PM Accelerator description displayed in app
- [x] Requirements file (backend/requirements/, frontend/package.json)
- [x] README with setup instructions
- [ ] Demo video (Phase 15)

---

## Architecture

See [docs/architecture.md](docs/architecture.md) for the full system diagram and data flow.

---

## Running Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```
