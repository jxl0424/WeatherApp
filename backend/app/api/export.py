from fastapi import APIRouter, Depends, Query
from fastapi.responses import PlainTextResponse, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import export_service

router = APIRouter(prefix="/weather/export", tags=["export"])

FORMAT_CSV = "csv"
FORMAT_JSON = "json"
FORMAT_MD = "md"


@router.get("", response_class=Response)
def export_data(
    format: str = Query(default=FORMAT_CSV, pattern=f"^({FORMAT_CSV}|{FORMAT_JSON}|{FORMAT_MD})$"),
    db: Session = Depends(get_db),
) -> Response:
    if format == FORMAT_JSON:
        content = export_service.export_json(db)
        return Response(
            content=content,
            media_type="application/json",
            headers={"Content-Disposition": 'attachment; filename="weather_searches.json"'},
        )

    if format == FORMAT_MD:
        content = export_service.export_markdown(db)
        return Response(
            content=content,
            media_type="text/markdown",
            headers={"Content-Disposition": 'attachment; filename="weather_searches.md"'},
        )

    content = export_service.export_csv(db)
    return Response(
        content=content,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="weather_searches.csv"'},
    )
