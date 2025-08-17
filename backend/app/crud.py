# backend/app/crud.py
from sqlalchemy.orm import Session
from . import models

# Whitelist of updatable/creatable fields
_ALLOWED_FIELDS = {
    "location_name", "latitude", "longitude",
    "start_date", "end_date",
    "temperature", "humidity", "recorded_at",
    "weather_data",
}

def _filtered_kwargs(kwargs: dict) -> dict:
    # keep only allowed keys
    return {k: v for k, v in kwargs.items() if k in _ALLOWED_FIELDS}

# Create
def create_weather_history(db: Session, **kwargs):
    data = _filtered_kwargs(kwargs)
    obj = models.WeatherHistory(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# Read all
def get_weather_history(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WeatherHistory).offset(skip).limit(limit).all()

# Read single by ID
def get_weather_history_by_id(db: Session, record_id: int):
    return db.query(models.WeatherHistory).filter(models.WeatherHistory.id == record_id).first()

# Read by location & optional date range
def get_weather_history_by_location(db: Session, location: str, start_date=None, end_date=None):
    query = db.query(models.WeatherHistory).filter(models.WeatherHistory.location_name == location)
    if start_date:
        query = query.filter(models.WeatherHistory.start_date >= start_date)
    if end_date:
        query = query.filter(models.WeatherHistory.end_date <= end_date)
    return query.all()

# Update (ignore unknown keys; ignore None values so partial updates are safe)
def update_weather_history(db: Session, record_id: int, **kwargs):
    obj = get_weather_history_by_id(db, record_id)
    if not obj:
        return None
    for key, value in _filtered_kwargs(kwargs).items():
        if value is not None:
            setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

# Delete
def delete_weather_history(db: Session, record_id: int):
    obj = get_weather_history_by_id(db, record_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
