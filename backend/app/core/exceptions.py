from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    status_code: int = 500
    code: str = "internal_error"

    def __init__(self, detail: str, fields: dict | None = None):
        self.detail = detail
        self.fields = fields
        super().__init__(detail)


class LocationNotFoundError(AppError):
    status_code = 404
    code = "location_not_found"


class WeatherSearchNotFoundError(AppError):
    status_code = 404
    code = "not_found"


class UpstreamWeatherError(AppError):
    status_code = 502
    code = "upstream_error"


class AIUnavailableError(AppError):
    status_code = 503
    code = "ai_unavailable"


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "code": exc.code, "fields": exc.fields},
    )
