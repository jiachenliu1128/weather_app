# youtube_api.py
import os
import httpx
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

def search_youtube_videos(
    query: str,
    max_results: int = 3
) -> List[Dict[str, Any]]:
    """
    Search YouTube for a given query, return a list of video titles and IDs.
    
    Args:
        query: The search query string
        max_results: The maximum number of results to return (default is 3)
        
    Returns:
        A list of dictionaries containing video IDs, titles, descriptions, and thumbnail URLs.
    """
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_KEY
    }
    resp = httpx.get(YOUTUBE_SEARCH_URL, params=params, timeout=10.0)
    resp.raise_for_status()
    data = resp.json()

    results: List[Dict[str, Any]] = []
    for item in data.get("items", []):
        vid_id = item["id"]["videoId"]
        snippet = item["snippet"]
        results.append({
            "video_id": vid_id,
            "title": snippet["title"],
            "description": snippet["description"],
            "watch_url": f"https://www.youtube.com/watch?v={vid_id}"
        })
    return results