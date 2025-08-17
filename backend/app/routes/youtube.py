# backend/app/routes/youtube.py
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..utils.youtube_api import search_youtube_videos, YouTubeAPIError

router = APIRouter(prefix="/youtube", tags=["youtube"])

@router.get("/{location}")
async def youtube_for_location(
    location: str,
    topic: Optional[str] = Query(default=None, description="Optional topic e.g. 'travel' or 'weather'"),
    max_results: int = Query(default=8, ge=1, le=25),
):
    """
    Returns a list of YouTube videos relevant to the location (and optional topic).
    """
    q = location if not topic else f"{location} {topic}"
    try:
        items = await search_youtube_videos(q, max_results=max_results)
        return {"query": q, "results": items}
    except YouTubeAPIError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"YouTube API error: {e}")
