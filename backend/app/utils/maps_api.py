# backend/app/utils/maps_api.py
# Server-side static map helpers (no API key)
from typing import Optional
from urllib.parse import urlencode

from ..utils.geocoding_api import geocode_text

def build_backend_static_url(
    lat: float,
    lon: float,
    *,
    zoom: int = 12,
    width: int = 600,
    height: int = 400,
) -> str:
    """
    Build the backend proxy URL that renders a static map PNG from OSM tiles.
    """
    zoom = max(1, min(int(zoom), 18))
    width = max(200, min(int(width), 2000))   # allow higher outputs
    height = max(200, min(int(height), 2000))
    params = {
        "lat": lat,
        "lon": lon,
        "zoom": zoom,
        "width": width,
        "height": height,
        # 'scale' intentionally omitted here and appended by routes
    }
    return f"/maps/by-coords/image?{urlencode(params)}"


async def map_image_for_location(
    query: str,
    *,
    zoom: int = 12,
    width: int = 600,
    height: int = 400,
) -> Optional[dict]:
    """
    Geocodes a free-text location, then returns a backend-rendered static image URL + coords + label.
    """
    results = await geocode_text(query, limit=1)
    if not results:
        return None
    lat = results[0]["lat"]
    lon = results[0]["lon"]
    label = results[0]["formatted"]
    url = build_backend_static_url(lat, lon, zoom=zoom, width=width, height=height)
    return {
        "query": query,
        "label": label,
        "lat": lat,
        "lon": lon,
        # Pointing directly to backend renderer so <img> loads reliably
        "static_map_url": url,
        "proxy_image_url": url,
        "attribution": "© OpenStreetMap contributors",
    }
