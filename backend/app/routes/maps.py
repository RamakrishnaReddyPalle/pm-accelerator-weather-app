# backend/app/routes/maps.py
from fastapi import APIRouter, HTTPException, Query, Response
from io import BytesIO
from functools import lru_cache

from ..utils.maps_api import map_image_for_location, build_backend_static_url
from ..config import settings  # uses TILE_SERVER_URL if set

# ---- server-side static rendering (no API key) ----
# Requires: pip install staticmap pillow requests
from staticmap import StaticMap, CircleMarker

router = APIRouter(prefix="/maps", tags=["maps"])

# ---- Tunables ----
_MAX_DIM = 2000          # allow higher-res renders
_MAX_SCALE = 3           # 1..3
_DEFAULT_MARKER_BASE = 12  # marker radius baseline


def _clamp_int(v: int, lo: int, hi: int) -> int:
    return max(lo, min(int(v), hi))


def _round_coord(x: float, places: int = 5) -> float:
    return float(f"{x:.{places}f}")


def _tile_server_templates() -> list[str]:
    """
    Ordered list of tile server templates to try. First is your config,
    then robust fallbacks (OSM main and subdomains).
    """
    templates: list[str] = []
    cfg = getattr(settings, "TILE_SERVER_URL", "").strip()
    if cfg:
        templates.append(cfg)
    # Fallbacks (safe, single-template variants; staticmap doesn't handle {s})
    templates.extend([
        "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "https://b.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "https://c.tile.openstreetmap.org/{z}/{x}/{y}.png",
    ])
    # Deduplicate while preserving order
    seen = set()
    ordered = []
    for t in templates:
        if t not in seen:
            ordered.append(t)
            seen.add(t)
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
    """
    Actual renderer. Renders at width*scale x height*scale with a scaled marker.
    Coordinates for StaticMap are (lon, lat).
    """
    # upscale canvas for HiDPI sharpness
    render_w = width * scale
    render_h = height * scale

    smap = StaticMap(
        render_w,
        render_h,
        url_template=url_template,
    )

    marker_radius = max(8, _DEFAULT_MARKER_BASE * scale)
    smap.add_marker(CircleMarker((lon, lat), "#d00", marker_radius))
    image = smap.render(zoom=zoom, center=(lon, lat))  # center is (lon, lat)

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
    """
    Cache the final PNG for identical requests.
    lat_r/lon_r are rounded coordinates to reduce cache fragmentation.
    tiles is the tile server URL template; include in key so different templates don't collide.
    """
    return _render_static_png_internal(
        lat=lat_r,
        lon=lon_r,
        zoom=zoom,
        width=width,
        height=height,
        scale=scale,
        url_template=tiles,
    )


def _render_static_png(
    lat: float,
    lon: float,
    *,
    zoom: int = 12,
    width: int = 600,
    height: int = 400,
    scale: int = 1,
) -> bytes:
    """
    Public wrapper that clamps, rounds, and caches. Tries multiple tile servers before failing.
    """
    zoom = _clamp_int(zoom, 1, 18)
    width = _clamp_int(width, 200, _MAX_DIM)
    height = _clamp_int(height, 200, _MAX_DIM)
    scale = _clamp_int(scale, 1, _MAX_SCALE)

    # Round coords to 5 dp to improve cache hits without visible change
    lat_r = _round_coord(lat, 5)
    lon_r = _round_coord(lon, 5)

    errors: list[str] = []
    for tpl in _tile_server_templates():
        try:
            return _render_cached(lat_r, lon_r, zoom, width, height, scale, tpl)
        except Exception as e:
            errors.append(f"{tpl} -> {e}")

    # If all templates failed, surface a concise error with the last few messages
    msg = " ; ".join(errors[-3:])
    raise RuntimeError(f"All tile servers failed: {msg}")


@router.get("/by-coords")
async def static_map_by_coords(
    lat: float = Query(...),
    lon: float = Query(...),
    zoom: int = Query(default=12, ge=1, le=18),
    width: int = Query(default=600, ge=200, le=2000),
    height: int = Query(default=400, ge=200, le=2000),
    scale: int = Query(default=1, ge=1, le=3),
):
    """
    Returns JSON pointing to the backend-rendered static map image (no external API key).
    Declared BEFORE /{location} so it isn't shadowed by the dynamic route.
    """
    try:
        base = build_backend_static_url(lat, lon, zoom=zoom, width=width, height=height)
        url = f"{base}&scale={scale}"
        return {
            "label": f"{lat:.5f}, {lon:.5f}",
            "lat": lat,
            "lon": lon,
            "static_map_url": url,     # frontend <img src=...>
            "proxy_image_url": url,    # same as static_map_url
            "attribution": "© OpenStreetMap contributors",
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Map generation failed: {e}")


@router.get("/by-coords/image")
async def static_map_by_coords_image(
    lat: float = Query(...),
    lon: float = Query(...),
    zoom: int = Query(default=12, ge=1, le=18),
    width: int = Query(default=600, ge=200, le=2000),
    height: int = Query(default=400, ge=200, le=2000),
    scale: int = Query(default=1, ge=1, le=3),
):
    """
    Streams a PNG generated from OSM tiles using the 'staticmap' library.
    Renders at width*scale x height*scale for crisper output on HiDPI.
    """
    try:
        png = _render_static_png(lat, lon, zoom=zoom, width=width, height=height, scale=scale)
        return Response(content=png, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Render error: {e}")


@router.get("/{location}")
async def static_map_for_location(
    location: str,
    zoom: int = Query(default=12, ge=1, le=18),
    width: int = Query(default=600, ge=200, le=2000),
    height: int = Query(default=400, ge=200, le=2000),
    scale: int = Query(default=1, ge=1, le=3),
):
    """
    Geocodes a free-text location and returns JSON with a backend-rendered static map URL.
    """
    try:
        result = await map_image_for_location(location, zoom=zoom, width=width, height=height)
        if not result:
            raise HTTPException(status_code=404, detail="Location not found")

        # Ensure current params in URLs
        base = build_backend_static_url(result["lat"], result["lon"], zoom=zoom, width=width, height=height)
        result["static_map_url"] = f"{base}&scale={scale}"
        result["proxy_image_url"] = result["static_map_url"]
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Map generation failed: {e}")
