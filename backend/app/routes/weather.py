# Weather endpoints
from fastapi import APIRouter, HTTPException
from ..schemas import (
    LocationQuery,
    ForecastRequest,
    CurrentWeatherResponse,
    ForecastResponse,
)
from ..utils.geocoding_api import geocode_text
from ..utils.weather_api import current_weather_by_coords, forecast_by_coords

router = APIRouter(prefix="/weather", tags=["weather"])

async def _resolve_location(payload: LocationQuery):
    """Resolve input into (lat, lon, name)."""
    # If coords provided, use
    if payload.lat is not None and payload.lon is not None:
        return payload.lat, payload.lon, None

    if payload.zip_code:
        q = f"{payload.zip_code} {payload.country_code or ''}".strip()
        results = await geocode_text(q, limit=1)
        if not results:
            raise HTTPException(status_code=404, detail="Location not found for zip")
        r = results[0]
        return r["lat"], r["lon"], r.get("formatted")

    # Free-text query:
    if payload.query:
        results = await geocode_text(payload.query, limit=1)
        if not results:
            raise HTTPException(status_code=404, detail="Location not found")
        r = results[0]
        return r["lat"], r["lon"], r.get("formatted")

    raise HTTPException(status_code=400, detail="Provide lat/lon, zip_code, or query")

@router.post("/current", response_model=CurrentWeatherResponse)
async def current_weather(payload: LocationQuery):
    if not payload.has_location():
        raise HTTPException(status_code=400, detail="No location provided")
    lat, lon, name = await _resolve_location(payload)
    try:
        data = await current_weather_by_coords(lat, lon, units=payload.units)
        # Prefer geocoded formatted name if available
        if name:
            data["location"]["name"] = name
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Weather API failed: {e}")

@router.post("/forecast", response_model=ForecastResponse)
async def forecast(payload: ForecastRequest):
    if not payload.has_location():
        raise HTTPException(status_code=400, detail="No location provided")
    lat, lon, name = await _resolve_location(LocationQuery(**payload.model_dump()))
    try:
        data = await forecast_by_coords(lat, lon, units=payload.units, days=payload.days)
        if name:
            data["location"]["name"] = name
        return data
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Weather API failed: {e}")
