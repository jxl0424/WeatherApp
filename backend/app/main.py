from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api import advice, export, integrations, weather
from app.core.config import settings
from app.core.exceptions import AppError, app_error_handler
from app.db.session import SessionLocal

_OPENAPI_TAGS = [
    {"name": "weather", "description": "Current weather, forecasts, and saved search CRUD"},
    {"name": "advice", "description": "AI travel recommendations powered by NVIDIA NIM"},
    {"name": "integrations", "description": "Raw geocoding and air quality pass-through"},
    {"name": "export", "description": "Export saved searches as CSV, JSON, or Markdown"},
    {"name": "health", "description": "Service and database liveness"},
]

app = FastAPI(
    title="AI Weather Travel Advisor",
    description="Weather search, CRUD, AI travel recommendations, and air quality — all in one.",
    version="1.0.0",
    openapi_tags=_OPENAPI_TAGS,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppError, app_error_handler)

API_PREFIX = "/api/v1"
app.include_router(export.router, prefix=API_PREFIX)
app.include_router(weather.router, prefix=API_PREFIX)
app.include_router(advice.router, prefix=API_PREFIX)
app.include_router(integrations.router, prefix=API_PREFIX)


@app.get("/health", tags=["health"], summary="Service and database liveness check")
def health() -> dict:
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "unavailable"
    finally:
        db.close()
    return {"status": "ok", "db": db_status}
