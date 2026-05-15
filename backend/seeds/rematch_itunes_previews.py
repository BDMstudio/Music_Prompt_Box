#!/usr/bin/env python3
"""
Rematch iTunes preview audio with strict genre validation.
Each style gets a hand-picked search targeting the definitive artist/track.
Results are rejected if iTunes genre label doesn't match expectations.
"""

import asyncio
import json
import sqlite3
import httpx
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "music_prompt_box.db"

# Hand-curated search map: style_id -> {search terms, expected iTunes genre, fallback}
# iTunes genre labels are limited: Pop, Rock, Dance, R&B/Soul, Hip-Hop/Rap, Electronic, 
# Alternative, Jazz, Country, Classical, Latin, J-Pop, K-Pop, etc.
STYLE_MATCHES = {
    "style_001": {
        "name": "Doo-Wop Romance",
        "searches": [
            {"term": "earth angel penguins", "genre": "R&B/Soul"},
            {"term": "in the still of the night five satins", "genre": "R&B/Soul"},
            {"term": "doo wop 50s only you platters", "genre": "R&B/Soul"},
        ],
        "accept_genres": ["R&B/Soul", "Oldies", "Pop"],
    },
    "style_002": {
        "name": "Rockabilly Jive",
        "searches": [
            {"term": "jailhouse rock elvis presley", "genre": "Rock"},
            {"term": "rock around the clock bill haley", "genre": "Rock"},
            {"term": "blue suede shoes carl perkins", "genre": "Rock"},
        ],
        "accept_genres": ["Rock", "Rock & Roll", "Oldies"],
    },
    "style_003": {
        "name": "Psychedelic Rock",
        "searches": [
            {"term": "purple haze jimi hendrix", "genre": "Rock"},
            {"term": "tomorrow never knows beatles", "genre": "Rock"},
            {"term": "white rabbit jefferson airplane", "genre": "Rock"},
        ],
        "accept_genres": ["Rock", "Alternative"],
    },
    "style_004": {
        "name": "Motown Soul",
        "searches": [
            {"term": "my girl temptations", "genre": "R&B/Soul"},
            {"term": "ain't no mountain diana ross", "genre": "R&B/Soul"},
            {"term": "i heard it through the grapevine marvin gaye", "genre": "R&B/Soul"},
        ],
        "accept_genres": ["R&B/Soul", "Pop"],
    },
    "style_005": {
        "name": "British Invasion",
        "searches": [
            {"term": "satisfaction rolling stones", "genre": "Rock"},
            {"term": "my generation the who", "genre": "Rock"},
            {"term": "house of the rising sun animals", "genre": "Rock"},
        ],
        "accept_genres": ["Rock"],
    },
    "style_006": {
        "name": "Classic Disco",
        "searches": [
            {"term": "stayin alive bee gees", "genre": "Dance"},
            {"term": "i will survive gloria gaynor", "genre": "Dance"},
            {"term": "le freak chic", "genre": "Dance"},
        ],
        "accept_genres": ["Dance", "Disco", "Pop"],
    },
    "style_007": {
        "name": "Hard Rock Anthem",
        "searches": [
            {"term": "whole lotta love led zeppelin", "genre": "Rock"},
            {"term": "highway star deep purple", "genre": "Rock"},
            {"term": "iron man black sabbath", "genre": "Rock"},
        ],
        "accept_genres": ["Rock", "Hard Rock", "Metal"],
    },
    "style_008": {
        "name": "Yacht Rock",
        "searches": [
            {"term": "what a fool believes doobie brothers", "genre": "Rock"},
            {"term": "sailing christopher cross", "genre": "Pop"},
            {"term": "ride like the wind christopher cross", "genre": "Pop"},
        ],
        "accept_genres": ["Rock", "Pop", "Soft Rock"],
    },
    "style_009": {
        "name": "Synthwave / Outrun",
        "searches": [
            {"term": "nightcall kavinsky", "genre": "Electronic"},
            {"term": "techdrive the midnight", "genre": "Electronic"},
            {"term": "turbo killer carpenter brut", "genre": "Electronic"},
        ],
        "accept_genres": ["Electronic", "Dance", "Alternative"],
    },
    "style_010": {
        "name": "Japanese City Pop",
        "searches": [
            {"term": "plastic love mariya takeuchi", "genre": "J-Pop"},
            {"term": "stay with me miki matsubara", "genre": "J-Pop"},
            {"term": "tadaima taeko ohnuki", "genre": "J-Pop"},
        ],
        "accept_genres": ["J-Pop", "Pop", "World"],
    },
    "style_011": {
        "name": "Post-Punk / Goth",
        "searches": [
            {"term": "love will tear us apart joy division", "genre": "Alternative"},
            {"term": "a forest the cure", "genre": "Alternative"},
            {"term": "bela lugosi's dead bauhaus", "genre": "Alternative"},
        ],
        "accept_genres": ["Alternative", "Rock"],
    },
    "style_012": {
        "name": "Boom Bap Hip-Hop",
        "searches": [
            {"term": "N.Y. State of Mind nas", "genre": "Hip-Hop/Rap"},
            {"term": "C.R.E.A.M. wu-tang clan", "genre": "Hip-Hop/Rap"},
            {"term": "shook ones mobb deep", "genre": "Hip-Hop/Rap"},
        ],
        "accept_genres": ["Hip-Hop/Rap"],
    },
    "style_013": {
        "name": "Seattle Grunge",
        "searches": [
            {"term": "smells like teen spirit nirvana", "genre": "Rock"},
            {"term": "black hole sun soundgarden", "genre": "Rock"},
            {"term": "alive pearl jam", "genre": "Rock"},
        ],
        "accept_genres": ["Rock", "Alternative"],
    },
    "style_014": {
        "name": "Eurodance",
        "searches": [
            {"term": "rhythm of the night corona", "genre": "Dance"},
            {"term": "mr vain culture beat", "genre": "Dance"},
            {"term": "what is love haddaway", "genre": "Dance"},
        ],
        "accept_genres": ["Dance", "Pop", "Electronic"],
    },
    "style_015": {
        "name": "Pop Punk",
        "searches": [
            {"term": "all the small things blink-182", "genre": "Rock"},
            {"term": "dammit blink-182", "genre": "Rock"},
            {"term": "my friends over you new found glory", "genre": "Rock"},
        ],
        "accept_genres": ["Rock", "Alternative", "Pop"],
    },
    "style_016": {
        "name": "Nu Metal",
        "searches": [
            {"term": "in the end linkin park", "genre": "Rock"},
            {"term": "korn blind", "genre": "Rock"},
            {"term": "chop suey system of a down", "genre": "Rock"},
        ],
        "accept_genres": ["Rock", "Hard Rock", "Metal", "Alternative"],
    },
    "style_017": {
        "name": "Festival EDM",
        "searches": [
            {"term": "animals martin garrix", "genre": "Dance"},
            {"term": "epic sandro silva", "genre": "Dance"},
            {"term": "tsunami dvbbs", "genre": "Dance"},
        ],
        "accept_genres": ["Dance", "Electronic"],
    },
    "style_018": {
        "name": "Lofi Hip Hop",
        "searches": [
            {"term": "nujabes feather", "genre": "Hip-Hop/Rap"},
            {"term": "lofi hip hop chill study", "genre": "Hip-Hop/Rap"},
            {"term": "coffee jinsang", "genre": "Hip-Hop/Rap"},
        ],
        "accept_genres": ["Hip-Hop/Rap", "Electronic", "New Age"],
    },
    "style_019": {
        "name": "Cyberpunk Phonk",
        "searches": [
            {"term": "murder in my mind kordhell", "genre": "Electronic"},
            {"term": "close eyes dvllc", "genre": "Electronic"},
            {"term": "phonk cowbell drift", "genre": "Electronic"},
        ],
        "accept_genres": ["Electronic", "Hip-Hop/Rap", "Dance"],
    },
    "style_020": {
        "name": "Hyperpop",
        "searches": [
            {"term": "money machine 100 gecs", "genre": "Alternative"},
            {"term": "good looking sleekgun", "genre": "Pop"},
            {"term": "ringtone charli xcx", "genre": "Pop"},
        ],
        "accept_genres": ["Alternative", "Pop", "Electronic"],
    },
}


async def search_itunes(client: httpx.AsyncClient, term: str, genre_hint: str) -> list:
    search_term = f"{term} {genre_hint}"
    params = {
        "term": search_term,
        "country": "US",
        "entity": "song",
        "limit": 10,
        "media": "music",
    }
    try:
        resp = await client.get("https://itunes.apple.com/search", params=params)
        resp.raise_for_status()
        data = resp.json()
        return [r for r in data.get("results", [])
                if r.get("wrapperType") == "track" and r.get("previewUrl")]
    except Exception as e:
        print(f"    SEARCH ERROR: {e}")
        return []


def validate_track(track: dict, accept_genres: list) -> bool:
    """Check if track's genre matches expectations."""
    track_genre = track.get("primaryGenreName", "")
    return track_genre in accept_genres


def pick_best_track(tracks: list, accept_genres: list, search_term: str) -> dict | None:
    """Pick the best track: prefer genre match, then closest name match."""
    genre_matched = [t for t in tracks if validate_track(t, accept_genres)]
    pool = genre_matched if genre_matched else tracks

    if not pool:
        return None

    # Among matched, prefer tracks where artist appears in search term
    search_lower = search_term.lower()
    for t in pool:
        if t.get("artistName", "").lower() in search_lower:
            return t

    # Fallback: first genre-matched track
    return pool[0]


async def main():
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    matched = 0
    failed = 0

    async with httpx.AsyncClient(timeout=10.0) as client:
        for style_id, info in STYLE_MATCHES.items():
            row = c.execute("SELECT name FROM styles WHERE id = ?", (style_id,)).fetchone()
            if not row:
                continue

            style_name = info["name"]
            print(f"\n{style_id}: {style_name}")

            best_track = None
            for search_cfg in info["searches"]:
                print(f"  Trying: '{search_cfg['term']}' [{search_cfg['genre']}]")
                tracks = await search_itunes(client, search_cfg["term"], search_cfg["genre"])
                
                track = pick_best_track(tracks, info["accept_genres"], search_cfg["term"])
                if track:
                    is_genre_match = validate_track(track, info["accept_genres"])
                    print(f"    -> {track['trackName']} - {track['artistName']} [{track.get('primaryGenreName', '?')}] {'OK' if is_genre_match else 'GENRE MISMATCH'}")
                    if is_genre_match:
                        best_track = track
                        break
                    elif not best_track:
                        best_track = track  # keep as fallback, try next
                else:
                    print(f"    -> No results")

                await asyncio.sleep(0.3)

            if best_track:
                artwork = best_track.get("artworkUrl100", "")
                artwork600 = artwork.replace("100x100", "600x600") if artwork else None

                metadata = json.dumps({
                    "platform": "itunes",
                    "track_id": best_track["trackId"],
                    "track_name": best_track["trackName"],
                    "artist_name": best_track["artistName"],
                    "artwork_url": artwork600,
                    "preview_url": best_track["previewUrl"],
                }, ensure_ascii=False)

                c.execute(
                    """UPDATE styles SET
                       audio_type = 'url',
                       audio_source = ?,
                       audio_platform = 'itunes',
                       audio_metadata = ?
                       WHERE id = ?""",
                    (best_track["previewUrl"], metadata, style_id)
                )
                conn.commit()
                matched += 1
                genre_ok = validate_track(best_track, info["accept_genres"])
                status = "GENRE OK" if genre_ok else "GENRE WARN"
                print(f"  >> FINAL: {best_track['trackName']} - {best_track['artistName']} [{best_track.get('primaryGenreName', '?')}] {status}")
            else:
                failed += 1
                print(f"  >> FAILED: No suitable match found")

            await asyncio.sleep(0.5)

    conn.close()
    print(f"\n{'='*60}")
    print(f"Done: {matched} matched, {failed} failed")


if __name__ == "__main__":
    asyncio.run(main())
