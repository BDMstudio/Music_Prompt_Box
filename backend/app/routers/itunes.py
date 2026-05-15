# File: backend/app/routers/itunes.py
"""
iTunes Search API proxy — search tracks and return preview URLs.
Proxied through backend to avoid CORS issues and add genre-accurate search hints.
"""

from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
import httpx

router = APIRouter(prefix="/api/itunes", tags=["itunes"])

ITUNES_SEARCH_URL = "https://itunes.apple.com/search"
ITUNES_LOOKUP_URL = "https://itunes.apple.com/lookup"


class iTunesTrack(BaseModel):
    track_id: int
    track_name: str
    artist_name: str
    collection_name: Optional[str] = None
    preview_url: Optional[str] = None
    artwork_url100: Optional[str] = None
    artwork_url600: Optional[str] = None
    track_time_ms: Optional[int] = None
    primary_genre_name: Optional[str] = None
    country: Optional[str] = None


class iTunesSearchResponse(BaseModel):
    result_count: int
    tracks: List[iTunesTrack]


def _to_itunes_track(item: dict) -> iTunesTrack:
    """Convert raw iTunes API item to our schema."""
    artwork = item.get("artworkUrl100", "")
    # Get higher-res artwork (600x600 instead of 100x100)
    artwork600 = artwork.replace("100x100", "600x600") if artwork else None
    return iTunesTrack(
        track_id=item.get("trackId", 0),
        track_name=item.get("trackName", ""),
        artist_name=item.get("artistName", ""),
        collection_name=item.get("collectionName"),
        preview_url=item.get("previewUrl"),
        artwork_url100=artwork,
        artwork_url600=artwork600,
        track_time_ms=item.get("trackTimeMillis"),
        primary_genre_name=item.get("primaryGenreName"),
        country=item.get("country"),
    )


@router.get("/search", response_model=iTunesSearchResponse)
async def search_tracks(
    term: str = Query(..., min_length=1, max_length=200, description="Search term, e.g. 'synthwave'"),
    country: str = Query("US", max_length=5, description="ISO country code, e.g. US, CN, JP, GB"),
    entity: str = Query("song", description="Entity type: song, musicArtist, album"),
    limit: int = Query(10, ge=1, le=25, description="Max results (1-25)"),
    genre: Optional[str] = Query(None, description="Genre hint to improve accuracy, e.g. 'Electronic'"),
):
    """
    Search iTunes Music catalog.
    When genre hint is provided, it's appended to the search term to improve result relevance.
    """
    # Build search term with genre hint for better accuracy
    search_term = term
    if genre:
        search_term = f"{term} {genre}"

    params = {
        "term": search_term,
        "country": country,
        "entity": entity,
        "limit": limit,
        "media": "music",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(ITUNES_SEARCH_URL, params=params)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=502,
                detail=f"iTunes API request failed: {str(e)}"
            )

    data = resp.json()
    tracks = [_to_itunes_track(item) for item in data.get("results", [])
              if item.get("wrapperType") == "track" and item.get("previewUrl")]

    return iTunesSearchResponse(
        result_count=len(tracks),
        tracks=tracks,
    )


@router.get("/lookup", response_model=iTunesSearchResponse)
async def lookup_track(
    id: int = Query(..., description="iTunes track ID"),
):
    """Look up a specific track by iTunes track ID."""
    params = {"id": id, "entity": "song"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(ITUNES_LOOKUP_URL, params=params)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=502,
                detail=f"iTunes API request failed: {str(e)}"
            )

    data = resp.json()
    tracks = [_to_itunes_track(item) for item in data.get("results", [])
              if item.get("wrapperType") == "track" and item.get("previewUrl")]

    return iTunesSearchResponse(
        result_count=len(tracks),
        tracks=tracks,
    )
