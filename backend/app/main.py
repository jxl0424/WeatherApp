from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import advice, export, integrations, weather
from app.core.config import settings
from app.core.exceptions import AppError, app_error_handler

app = FastAPI(
    title="AI Weather Travel Advisor",
    description="Weather search, CRUD, AI travel recommendations, and air quality — all in one.",
    version="1.0.0",
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
app.include_router(weather.router, prefix=API_PREFIX)
app.include_router(advice.router, prefix=API_PREFIX)
app.include_router(export.router, prefix=API_PREFIX)
app.include_router(integrations.router, prefix=API_PREFIX)


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok"}
