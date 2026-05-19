#!/usr/bin/env python3
"""
Add new style cards to the database with iTunes preview audio.
Usage: python add_styles.py
"""

import asyncio
import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# ── Style data to insert ──
NEW_STYLES = [
    # ═══ Funk (genre_1970s_funk) ═══
    {
        "name": "P-Funk / Parliament Funk",
        "tags": ["p-funk", "parliament funkadelic", "synth bass", "clavinet", "collective groove", "cosmic slop"],
        "genre_id": "genre_1970s_funk",
        "description": "乔治·克林顿主导的议会放克，宇宙感集体即兴",
        "bpm_range": "90-110",
        "itunes_search": "Parliament Give Up The Funk"
    },
    {
        "name": "James Brown Funk",
        "tags": ["james brown funk", "tight horns", "syncopated rhythm", "on the one", "brass stabs", "dynamic groove"],
        "genre_id": "genre_1970s_funk",
        "description": "詹姆士·布朗式紧绷放克，铜管与切分节奏驱动",
        "bpm_range": "100-120",
        "itunes_search": "James Brown Get Up I Feel Like Being A Sex Machine"
    },
    {
        "name": "Boogie Funk",
        "tags": ["boogie funk", "80s groove", "synth bass", "roland jupiter", "slap bass", "roller skate vibe"],
        "genre_id": "genre_1970s_funk",
        "description": "70年代末至80年代初合成器放克，旱冰场氛围",
        "bpm_range": "105-120",
        "itunes_search": "Zapp More Bounce To The Ounce"
    },
    {
        "name": "Afrobeat Fusion",
        "tags": ["afrobeat", "fela kuti", "polyrhythm", "horn section", "call and response", "extended groove"],
        "genre_id": "genre_1970s_funk",
        "description": "非洲节奏与放克融合，多重节奏层叠",
        "bpm_range": "95-115",
        "itunes_search": "Fela Kuti Zombie"
    },
    # ═══ New Wave (genre_1980s_newwave) ═══
    {
        "name": "Synthpop / Electropop",
        "tags": ["synthpop", "electropop", "yamaha dx7", "drum machine", "catchy hook", "new romantic"],
        "genre_id": "genre_1980s_newwave",
        "description": "合成器流行，浪漫旋律与电子音色交织",
        "bpm_range": "110-135",
        "itunes_search": "Duran Duran Hungry Like The Wolf"
    },
    {
        "name": "Darkwave / Minimal Wave",
        "tags": ["darkwave", "minimal wave", "cold synth", "monotone vocal", "industrial edge", "coldwave"],
        "genre_id": "genre_1980s_newwave",
        "description": "暗黑浪潮，冰冷合成器与机械节奏",
        "bpm_range": "100-130",
        "itunes_search": "Depeche Mode Just Cant Get Enough"
    },
    {
        "name": "New Wave Rock",
        "tags": ["new wave rock", "jangle pop", "angular guitar", "quirky vocal", "power pop", "skinny tie"],
        "genre_id": "genre_1980s_newwave",
        "description": "新浪潮摇滚，棱角吉他与怪趣人声",
        "bpm_range": "120-150",
        "itunes_search": "The Cars Just What I Needed"
    },
    {
        "name": "Dance-Pop / Hi-NRG",
        "tags": ["dance pop", "hi-nrg", "four on the floor", "diva vocal", "synth arpeggio", "club hit"],
        "genre_id": "genre_1980s_newwave",
        "description": "舞曲流行，迪斯科遗产与电子节拍融合",
        "bpm_range": "120-140",
        "itunes_search": "Madonna Into The Groove"
    },
    # ═══ Trap (genre_2010s_trap) ═══
    {
        "name": "Atlanta Trap",
        "tags": ["atlanta trap", "808 bass", "hi-hat rolls", "trap hi hats", "dark melody", "migos flow"],
        "genre_id": "genre_2010s_trap",
        "description": "亚特兰大陷阱，标志性 808 低音与碎镲",
        "bpm_range": "130-160",
        "itunes_search": "Migos Bad and Boujee"
    },
    {
        "name": "Melodic Trap",
        "tags": ["melodic trap", "auto-tune vocal", "ambient pad", "emotional melody", "808 sub bass", "nocturnal"],
        "genre_id": "genre_2010s_trap",
        "description": "旋律陷阱，Auto-Tune 人声与氛围音景",
        "bpm_range": "120-145",
        "itunes_search": "Travis Scott SICKO MODE"
    },
    {
        "name": "UK Drill",
        "tags": ["uk drill", "sliding 808", "skittering hi hats", "dark piano", "london flow", "aggressive"],
        "genre_id": "genre_2010s_trap",
        "description": "英国 Drill，滑音 808 与暗黑钢琴",
        "bpm_range": "140-150",
        "itunes_search": "Headie One Both"
    },
    {
        "name": "Trap Soul",
        "tags": ["trap soul", "r&b vocals", "lush pads", "slow trap beat", "intimate", "bryson tiller"],
        "genre_id": "genre_2010s_trap",
        "description": "陷阱灵魂，R&B 人声与慢速陷阱节拍",
        "bpm_range": "90-115",
        "itunes_search": "Bryson Tiller Dont"
    },
    # ═══ Bedroom Pop (genre_2020s_bedroom) ═══
    {
        "name": "Lo-Fi Bedroom Pop",
        "tags": ["bedroom pop", "lo-fi guitar", "reverb vocal", "diy production", "cassette tape", "dreamy"],
        "genre_id": "genre_2020s_bedroom",
        "description": "低保真卧室流行，磁带质感与梦幻人声",
        "bpm_range": "80-110",
        "itunes_search": "Clairo Pretty Girl"
    },
    {
        "name": "Dream Pop / Shoegaze DIY",
        "tags": ["dream pop", "shoegaze diy", "reverb wall", "ethereal vocal", "jangle guitar", "hazy"],
        "genre_id": "genre_2020s_bedroom",
        "description": "梦幻流行 DIY，混响墙与空灵人声",
        "bpm_range": "85-115",
        "itunes_search": "Beach House Space Song"
    },
    {
        "name": "Indie Pop Bedroom",
        "tags": ["indie pop", "bedroom production", "ukulele", "soft synth", "quirky lyrics", "gen z aesthetic"],
        "genre_id": "genre_2020s_bedroom",
        "description": "独立流行卧室制作，轻盈合成器与清新旋律",
        "bpm_range": "95-125",
        "itunes_search": "Rex Orange County Sunflower"
    },
    {
        "name": "Hypnagogic Pop",
        "tags": ["hypnagogic pop", "vapor pop", "retro synth", "warped melody", "nostalgic glow", "slowed down"],
        "genre_id": "genre_2020s_bedroom",
        "description": "催眠流行，复古合成器与扭曲怀旧的温暖光晕",
        "bpm_range": "80-105",
        "itunes_search": "Mac De Marco Chamber Of Reflection"
    },
    # ═══ Punk Rock (genre_1970s_punk) ═══
    {
        "name": "77 Punk",
        "tags": ["77 punk", "raw power", "three chords", "fast tempo", "anti-establishment", "diy ethic"],
        "genre_id": "genre_1970s_punk",
        "description": "77 原始朋克，三个和弦的暴力美学",
        "bpm_range": "150-200",
        "itunes_search": "Sex Pistols Anarchy In The UK"
    },
    {
        "name": "Ramones Style Punk",
        "tags": ["ramones punk", "buzzsaw guitar", "bubblegum punk", "1-2-3-4 count", "short songs", "high energy"],
        "genre_id": "genre_1970s_punk",
        "description": "雷蒙斯式朋克，电锯吉他与泡泡糖旋律",
        "bpm_range": "160-200",
        "itunes_search": "Ramones Blitzkrieg Bop"
    },
    {
        "name": "Street Punk / Oi!",
        "tags": ["street punk", "oi", "football chant", "working class", "gang vocal", "boot boy"],
        "genre_id": "genre_1970s_punk",
        "description": "街头朋克 Oi！工人阶级合唱与粗犷力量",
        "bpm_range": "140-180",
        "itunes_search": "Sham 69 If The Kids Are United"
    },
    {
        "name": "Art Punk",
        "tags": ["art punk", "avant-garde", "dissonant chords", "spoken word", "no wave", "experimental"],
        "genre_id": "genre_1970s_punk",
        "description": "艺术朋克，前卫不和谐与实验态度",
        "bpm_range": "110-160",
        "itunes_search": "Talking Heads Psycho Killer"
    },
]


async def search_itunes(term: str, country: str = "US") -> dict | None:
    """Search iTunes API for a track, return first result with preview."""
    import httpx

    url = "https://itunes.apple.com/search"
    params = {
        "term": term,
        "country": country,
        "entity": "song",
        "limit": 5,
        "media": "music",
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
        except Exception as e:
            print(f"  [WARN] iTunes search failed for '{term}': {e}")
            return None

    data = resp.json()
    for item in data.get("results", []):
        if item.get("wrapperType") == "track" and item.get("previewUrl"):
            artwork = item.get("artworkUrl100", "")
            artwork600 = artwork.replace("100x100", "600x600") if artwork else None
            return {
                "platform": "itunes",
                "track_id": item.get("trackId", 0),
                "track_name": item.get("trackName", ""),
                "artist_name": item.get("artistName", ""),
                "artwork_url": artwork600 or artwork,
                "preview_url": item.get("previewUrl", ""),
            }

    print(f"  [WARN] No preview found for '{term}'")
    return None


async def add_styles():
    from app.database import AsyncSessionLocal
    from app.models import Style

    inserted = 0
    no_audio = 0

    async with AsyncSessionLocal() as session:
        for style_data in NEW_STYLES:
            style_id = f"style_{uuid.uuid4().hex[:8]}"

            # Search iTunes for preview
            audio_metadata = None
            audio_source = None
            audio_type = None
            audio_platform = None

            search_term = style_data.get("itunes_search", style_data["name"])
            print(f"Searching iTunes: {search_term} ...", end=" ")
            itunes_result = await search_itunes(search_term)

            if itunes_result:
                audio_metadata = json.dumps(itunes_result, ensure_ascii=False)
                audio_source = itunes_result["preview_url"]
                audio_type = "url"
                audio_platform = "itunes"
                print(f"OK -> {itunes_result['track_name']} by {itunes_result['artist_name']}")
            else:
                no_audio += 1
                print("NO PREVIEW")

            style = Style(
                id=style_id,
                name=style_data["name"],
                tags_json=json.dumps(style_data["tags"], ensure_ascii=False),
                genre_id=style_data["genre_id"],
                description=style_data["description"],
                bpm_range=style_data["bpm_range"],
                audio_type=audio_type,
                audio_source=audio_source,
                audio_platform=audio_platform,
                audio_metadata=audio_metadata,
                reference_url=None,
                copy_count=0,
            )
            session.add(style)
            inserted += 1

        await session.commit()

    print(f"\nDone! Inserted {inserted} styles ({no_audio} without audio preview)")


if __name__ == "__main__":
    asyncio.run(add_styles())
