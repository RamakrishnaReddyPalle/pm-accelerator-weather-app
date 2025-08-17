# YouTube API integration
# backend/app/utils/youtube_api.py
import httpx
from typing import List, Dict, Optional
from ..config import settings

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

class YouTubeAPIError(Exception):
    pass

async def search_youtube_videos(
    query: str,
    max_results: int = 8,
    safe_search: str = "moderate",
) -> List[Dict]:
    """
    Search YouTube videos by query using official Data API v3.
    Returns a list of simplified items with id/title/thumbnail/url/publishedAt/channelTitle.
    """
    if not settings.YOUTUBE_API_KEY:
        raise YouTubeAPIError("YouTube API key not configured")

    params = {
        "key": settings.YOUTUBE_API_KEY,
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max(1, min(max_results, 25)),
        "safeSearch": safe_search,
        "order": "relevance",
    }

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(YOUTUBE_SEARCH_URL, params=params)
        r.raise_for_status()
        data = r.json()

    items = []
    for item in data.get("items", []):
        vid = item.get("id", {}).get("videoId")
        sn = item.get("snippet", {})
        if not vid:
            continue
        items.append({
            "videoId": vid,
            "title": sn.get("title"),
            "description": sn.get("description"),
            "thumbnail": sn.get("thumbnails", {}).get("medium", {}).get("url")
                          or sn.get("thumbnails", {}).get("default", {}).get("url"),
            "url": f"https://www.youtube.com/watch?v={vid}",
            "publishedAt": sn.get("publishedAt"),
            "channelTitle": sn.get("channelTitle"),
        })
    return items
