#!/usr/bin/env python3
"""
Batch match iTunes preview audio for existing style cards.
Uses style name + genre name as search term to find accurate previews.
"""

import asyncio
import json
import sqlite3
import httpx
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "music_prompt_box.db"

# Search terms optimized for each style — hand-tuned for accuracy
STYLE_SEARCH_MAP = {
    "style_001": {"term": "doo wop 50s romance", "genre": "R&B/Soul"},
    "style_002": {"term": "rockabilly elvis", "genre": "Rock"},
    "style_003": {"term": "psychedelic rock jimi hendrix", "genre": "Rock"},
    "style_004": {"term": "motown soul stevie wonder", "genre": "R&B/Soul"},
    "style_005": {"term": "british invasion beatles", "genre": "Rock"},
    "style_006": {"term": "disco donna summer", "genre": "Dance"},
    "style_007": {"term": "hard rock led zeppelin", "genre": "Rock"},
    "style_008": {"term": "yacht rock michael mcdonald", "genre": "Rock"},
    "style_009": {"term": "synthwave outrun", "genre": "Electronic"},
    "style_010": {"term": "city pop tatsuro yamashita", "genre": "J-Pop"},
    "style_011": {"term": "post-punk joy division", "genre": "Alternative"},
    "style_012": {"term": "boom bap nas", "genre": "Hip-Hop/Rap"},
    "style_013": {"term": "grunge nirvana smells like teen spirit", "genre": "Rock"},
    "style_014": {"term": "eurodance 90s", "genre": "Dance"},
    "style_015": {"term": "pop punk blink 182", "genre": "Rock"},
    "style_016": {"term": "nu metal linkin park", "genre": "Rock"},
    "style_017": {"term": "big room edm martin garrix", "genre": "Dance"},
    "style_018": {"term": "lofi hip hop chill beats", "genre": "Hip-Hop/Rap"},
    "style_019": {"term": "phonk drift cowbell", "genre": "Hip-Hop/Rap"},
    "style_020": {"term": "hyperpop 100 gecs", "genre": "Pop"},
}


async def search_itunes(client: httpx.AsyncClient, term: str, genre: str) -> dict | None:
    """Search iTunes and return the best matching track."""
    search_term = f"{term} {genre}"
    params = {
        "term": search_term,
        "country": "US",
        "entity": "song",
        "limit": 5,
        "media": "music",
    }
    try:
        resp = await client.get("https://itunes.apple.com/search", params=params)
        resp.raise_for_status()
        data = resp.json()
        results = [r for r in data.get("results", [])
                   if r.get("wrapperType") == "track" and r.get("previewUrl")]
        if results:
            return results[0]
    except Exception as e:
        print(f"  ERROR: {e}")
    return None


async def main():
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    matched = 0
    failed = 0

    async with httpx.AsyncClient(timeout=10.0) as client:
        for style_id, search_info in STYLE_SEARCH_MAP.items():
            # Check if already has audio
            row = c.execute(
                "SELECT name, audio_source FROM styles WHERE id = ?",
                (style_id,)
            ).fetchone()
            if not row:
                print(f"  SKIP: {style_id} not found")
                continue
            style_name = row[0]
            if row[1]:  # already has audio
                print(f"  SKIP: {style_name} already has audio")
                continue

            print(f"  Searching: {style_name} -> '{search_info['term']}' ({search_info['genre']})")

            track = await search_itunes(client, search_info["term"], search_info["genre"])
            if track:
                artwork = track.get("artworkUrl100", "")
                artwork600 = artwork.replace("100x100", "600x600") if artwork else None

                metadata = json.dumps({
                    "platform": "itunes",
                    "track_id": track["trackId"],
                    "track_name": track["trackName"],
                    "artist_name": track["artistName"],
                    "artwork_url": artwork600,
                    "preview_url": track["previewUrl"],
                }, ensure_ascii=False)

                c.execute(
                    """UPDATE styles SET
                       audio_type = 'url',
                       audio_source = ?,
                       audio_platform = 'itunes',
                       audio_metadata = ?
                       WHERE id = ?""",
                    (track["previewUrl"], metadata, style_id)
                )
                conn.commit()
                matched += 1
                print(f"    -> Matched: {track['trackName']} - {track['artistName']} [{track.get('primaryGenreName', '?')}]")
            else:
                failed += 1
                print(f"    -> NO MATCH")

            # Small delay to be respectful to iTunes API
            await asyncio.sleep(0.5)

    conn.close()
    print(f"\nDone: {matched} matched, {failed} failed")


if __name__ == "__main__":
    asyncio.run(main())
