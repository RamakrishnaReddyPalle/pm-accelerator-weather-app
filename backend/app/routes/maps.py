# backend/app/routes/maps.py
from fastapi import APIRouter, HTTPException, Query, Response
from io import BytesIO
from functools import lru_cache

from ..utils.maps_api import map_image_for_location, build_backend_static_url
from ..config import settings
from staticmap import StaticMap, CircleMarker

router = APIRouter(prefix="/maps", tags=["maps"])

_MAX_DIM = 2000
_MAX_SCALE = 3
_DEFAULT_MARKER_BASE = 12

def _clamp_int(v: int, lo: int, hi: int) -> int:
    return max(lo, min(int(v), hi))

def _round_coord(x: float, places: int = 5) -> float:
    return float(f"{x:.{places}f}")

def _tile_server_templates() -> list[str]:
    """
    Prefer the main OSM tile servers first (robust),
    then try any custom TILE_SERVER_URL as a last resort.
    """
    ordered = [
        "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "https://b.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "https://c.tile.openstreetmap.org/{z}/{x}/{y}.png",
    ]
    cfg = getattr(settings, "TILE_SERVER_URL", "").strip()
    if cfg and cfg not in ordered:
        ordered.append(cfg)
    return ordered

def _render_static_png_internal(
    lat: float,
    lon: float,
    *,
    zoom: int,
    width: int,
    height: int,
    scale: int,
    url_template: str,
) -> bytes:
    render_w = width * scale
    render_h = height * scale
    smap = StaticMap(render_w, render_h, url_template=url_template)

    marker_radius = max(8, _DEFAULT_MARKER_BASE * scale)
    smap.add_marker(CircleMarker((lon, lat), "#d00", marker_radius))

    image = smap.render(zoom=zoom, center=(lon, lat))
    buf = BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()

@lru_cache(maxsize=256)
def _render_cached(
    lat_r: float,
    lon_r: float,
    zoom: int,
    width: int,
    height: int,
    scale: int,
    tiles: str,
) -> bytes:
    return _render_static_png_internal(
        lat=lat_r, lon=lon_r,
        zoom=zoom, width=width, height=height, scale=scale,
        url_template=tiles,
    )

def _render_static_png(
    lat: float,
    lon: float,
    *,
    zoom: int = 13,          # tighter default to reduce tile count
    width: int = 640,        # a bit smaller than 800x500 for speed
    height: int = 400,
    scale: int = 1,          # crisp enough, fast to load
) -> bytes:
    zoom = _clamp_int(zoom, 1, 18)
    width = _clamp_int(width, 200, _MAX_DIM)
    height = _clamp_int(height, 200, _MAX_DIM)
    scale = _clamp_int(scale, 1, _MAX_SCALE)

    lat_r = _round_coord(lat, 5)
    lon_r = _round_coord(lon, 5)

    errors: list[str] = []
    for tpl in _tile_server_templates():
        try:
            return _render_cached(lat_r, lon_r, zoom, width, height, scale, tpl)
        except Exception as e:
            errors.append(f"{tpl} -> {e}")
    raise RuntimeError("All tile servers failed: " + " ; ".join(errors[-3:]))

@router.get("/by-coords")
async def static_map_by_coords(
    lat: float = Query(...),
    lon: float = Query(...),
    zoom: int = Query(default=13, ge=1, le=18),
    width: int = Query(default=640, ge=200, le=2000),
    height: int = Query(default=400, ge=200, le=2000),
    scale: int = Query(default=1, ge=1, le=3),
):
    try:
        base = build_backend_static_url(lat, lon, zoom=zoom, width=width, height=height)
        url = f"{base}&scale={scale}"
        return {
            "label": f"{lat:.5f}, {lon:.5f}",
            "lat": lat,
            "lon": lon,
            "static_map_url": url,
            "proxy_image_url": url,
            "attribution": "© OpenStreetMap contributors",
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Map generation failed: {e}")

@router.get("/by-coords/image")
async def static_map_by_coords_image(
    lat: float = Query(...),
    lon: float = Query(...),
    zoom: int = Query(default=13, ge=1, le=18),
    width: int = Query(default=640, ge=200, le=2000),
    height: int = Query(default=400, ge=200, le=2000),
    scale: int = Query(default=1, ge=1, le=3),
    format: str = Query(default="png", pattern="^(png|webp)$"),
):
    try:
        png_bytes = _render_static_png(lat, lon, zoom=zoom, width=width, height=height, scale=scale)

        headers = {"Cache-Control": "public, max-age=86400, immutable"}

        if format == "webp":
            from PIL import Image
            img = Image.open(BytesIO(png_bytes))
            out = BytesIO()
            img.save(out, format="WEBP", quality=80, method=6)
            return Response(content=out.getvalue(), media_type="image/webp", headers=headers)

        return Response(content=png_bytes, media_type="image/png", headers=headers)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Render error: {e}")

@router.get("/{location}")
async def static_map_for_location(
    location: str,
    zoom: int = Query(default=13, ge=1, le=18),
    width: int = Query(default=640, ge=200, le=2000),
    height: int = Query(default=400, ge=200, le=2000),
    scale: int = Query(default=1, ge=1, le=3),
):
    try:
        result = await map_image_for_location(location, zoom=zoom, width=width, height=height)
        if not result:
            raise HTTPException(status_code=404, detail="Location not found")

        base = build_backend_static_url(result["lat"], result["lon"], zoom=zoom, width=width, height=height)
        result["static_map_url"] = f"{base}&scale={scale}"
        result["proxy_image_url"] = result["static_map_url"]
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Map generation failed: {e}")

