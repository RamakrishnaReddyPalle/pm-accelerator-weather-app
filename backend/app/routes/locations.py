# Location search endpoints
from fastapi import APIRouter, HTTPException
from ..schemas import GeocodeRequest, GeocodeResponse, GeocodeCandidate
from ..utils.geocoding_api import geocode_text

router = APIRouter(prefix="/locations", tags=["locations"])

@router.post("/search", response_model=GeocodeResponse)
async def search_locations(payload: GeocodeRequest):
    try:
        results = await geocode_text(payload.query, limit=5)
        return {"candidates": [GeocodeCandidate(**r) for r in results]}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Geocoding failed: {e}")
