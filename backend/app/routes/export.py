# Data export endpoints
# backend/app/routes/export.py
from datetime import datetime, date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..utils.export_utils import (
    fetch_history, export_csv, export_json, export_xml, export_pdf
)

router = APIRouter(prefix="/export", tags=["export"])

def _parse_date(val: Optional[str]) -> Optional[date]:
    if not val:
        return None
    try:
        return datetime.strptime(val, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {val}. Use YYYY-MM-DD")

def _common_fetch(
    db: Session,
    location_name: Optional[str],
    start_date_str: Optional[str],
    end_date_str: Optional[str],
    limit: int,
    skip: int,
):
    start_date = _parse_date(start_date_str)
    end_date = _parse_date(end_date_str)
    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date cannot be after end_date")

    rows = fetch_history(
        db=db,
        location_name=location_name,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        skip=skip,
    )
    if not rows:
        # Return empty file but 200; or choose 204. We'll return tiny file so UX isn't confusing.
        pass
    return rows

@router.get("/csv")
def export_history_csv(
    location_name: Optional[str] = Query(default=None),
    start_date: Optional[str] = Query(default=None),
    end_date: Optional[str] = Query(default=None),
    limit: int = Query(default=1000, ge=1, le=50000),
    skip: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    rows = _common_fetch(db, location_name, start_date, end_date, limit, skip)
    content = export_csv(rows)
    filename = "weather_history.csv"
    return Response(
        content=content,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

@router.get("/json")
def export_history_json(
    location_name: Optional[str] = Query(default=None),
    start_date: Optional[str] = Query(default=None),
    end_date: Optional[str] = Query(default=None),
    limit: int = Query(default=1000, ge=1, le=50000),
    skip: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    rows = _common_fetch(db, location_name, start_date, end_date, limit, skip)
    content = export_json(rows)
    filename = "weather_history.json"
    return Response(
        content=content,
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

@router.get("/xml")
def export_history_xml(
    location_name: Optional[str] = Query(default=None),
    start_date: Optional[str] = Query(default=None),
    end_date: Optional[str] = Query(default=None),
    limit: int = Query(default=1000, ge=1, le=50000),
    skip: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    rows = _common_fetch(db, location_name, start_date, end_date, limit, skip)
    content = export_xml(rows)
    filename = "weather_history.xml"
    return Response(
        content=content,
        media_type="application/xml",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

@router.get("/pdf")
def export_history_pdf(
    location_name: Optional[str] = Query(default=None),
    start_date: Optional[str] = Query(default=None),
    end_date: Optional[str] = Query(default=None),
    limit: int = Query(default=1000, ge=1, le=50000),
    skip: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    rows = _common_fetch(db, location_name, start_date, end_date, limit, skip)
    content = export_pdf(rows, title="Weather History Export")
    filename = "weather_history.pdf"
    return Response(
        content=content,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

