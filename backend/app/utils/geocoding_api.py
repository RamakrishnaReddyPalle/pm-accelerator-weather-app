# Location search API (OpenCage/Mapbox)
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from ..config import settings

OPENCAGE_URL = "https://api.opencagedata.com/geocode/v1/json"

class GeocodingError(Exception):
    pass

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
async def geocode_text(query: str, limit: int = 5):
    """Geocode a free-text query using OpenCage."""
    if not settings.OPENCAGE_API_KEY:
        raise GeocodingError("OpenCage API key missing")
    params = {
        "q": query,
        "key": settings.OPENCAGE_API_KEY,
        "limit": limit,
        "no_annotations": 1,
        "language": "en",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(OPENCAGE_URL, params=params)
        r.raise_for_status()
        data = r.json()

    results = []
    for item in data.get("results", []):
        g = {
            "formatted": item.get("formatted"),
            "lat": item["geometry"]["lat"],
            "lon": item["geometry"]["lng"],
            "confidence": item.get("confidence"),
            "components": item.get("components", {}),
        }
        results.append(g)
    return results

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
async def reverse_geocode(lat: float, lon: float):
    """Reverse geocode coordinates → address using OpenCage."""
    if not settings.OPENCAGE_API_KEY:
        raise GeocodingError("OpenCage API key missing")
    params = {
        "q": f"{lat},{lon}",
        "key": settings.OPENCAGE_API_KEY,
        "limit": 1,
        "no_annotations": 1,
        "language": "en",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(OPENCAGE_URL, params=params)
        r.raise_for_status()
        data = r.json()

    if not data.get("results"):
        raise GeocodingError("No reverse geocoding result")

    item = data["results"][0]
    return {
        "formatted": item.get("formatted"),
        "lat": item["geometry"]["lat"],
        "lon": item["geometry"]["lng"],
        "components": item.get("components", {}),
    }
