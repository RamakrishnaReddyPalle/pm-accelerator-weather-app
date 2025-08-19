# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware  # <-- add
from sqlalchemy.orm import Session
from datetime import datetime

from .config import settings
from .database import Base, engine, get_db
from .routes import weather as weather_routes
from .routes import locations as locations_routes
from .routes import export as export_routes
from .routes import misc as misc_routes
from .routes import youtube as youtube_routes
from .routes import maps as maps_routes
from . import schemas, crud
from .utils.migrate_sqlite import ensure_history_columns

# Create DB tables (dev convenience; in prod use migrations)
Base.metadata.create_all(bind=engine)
ensure_history_columns(engine)

app = FastAPI(
    title="Weather App API",
    version="3.0.0",
    description="Phase 1: Weather & geocoding • Phase 2: History CRUD • Phase 3: YouTube & Static Maps",
)

origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# gzip (speeds up JSON & images)
app.add_middleware(GZipMiddleware, minimum_size=1024)

# Routers
app.include_router(weather_routes.router)
app.include_router(locations_routes.router)
app.include_router(export_routes.router)
app.include_router(misc_routes.router)
app.include_router(youtube_routes.router)
app.include_router(maps_routes.router)

@app.get("/", tags=["health"])
def health():
    return {"status": "ok"}

# ---- Phase 2: Weather History CRUD ----

@app.post("/weather/history", response_model=schemas.WeatherHistoryRead, tags=["history"])
def add_weather_record(record: schemas.WeatherHistoryCreate, db: Session = Depends(get_db)):
    return crud.create_weather_history(db, **record.model_dump())

@app.get("/weather/history", response_model=list[schemas.WeatherHistoryRead], tags=["history"])
def read_weather_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_weather_history(db, skip=skip, limit=limit)

@app.get("/weather/history/search", response_model=list[schemas.WeatherHistoryRead], tags=["history"])
def search_weather_history(
    location_name: str = Query(..., min_length=2, max_length=50),
    start_date: str = Query(...),
    end_date: str = Query(...),
    db: Session = Depends(get_db),
):
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    if start_date_obj > end_date_obj:
        raise HTTPException(status_code=400, detail="Start date cannot be after end date.")

    return crud.get_weather_history_by_location(
        db, location_name, start_date=start_date_obj, end_date=end_date_obj
    )

@app.put("/weather/history/{record_id}", response_model=schemas.WeatherHistoryRead, tags=["history"])
def update_weather_record(record_id: int, record: schemas.WeatherHistoryUpdate, db: Session = Depends(get_db)):
    updated = crud.update_weather_history(db, record_id, **record.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Record not found")
    return updated

@app.delete("/weather/history/{record_id}", response_model=schemas.WeatherHistoryRead, tags=["history"])
def delete_weather_record(record_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_weather_history(db, record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    return deleted
