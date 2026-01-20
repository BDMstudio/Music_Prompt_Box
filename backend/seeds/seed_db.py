# File: backend/seeds/seed_db.py

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import engine, AsyncSessionLocal, Base
from app.models import Genre, Style, Folder, FolderStyle


async def seed_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    seed_file = Path(__file__).parent / "initial_data.json"
    with open(seed_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    async with AsyncSessionLocal() as session:
        for genre_data in data["data"]["genres"]:
            genre = Genre(
                id=genre_data["id"],
                name=genre_data["name"],
                parent_id=genre_data.get("parent_id"),
                level=genre_data.get("level", 1),
                sort_order=genre_data.get("sort_order", 0),
                description=genre_data.get("description"),
                era_prompt=genre_data.get("era_prompt"),
            )
            session.add(genre)

        await session.commit()
        print(f"Seeded {len(data['data']['genres'])} genres")

        for style_data in data["data"]["styles"]:
            style = Style(
                id=style_data["id"],
                name=style_data["name"],
                tags_json=json.dumps(style_data.get("tags", []), ensure_ascii=False),
                genre_id=style_data.get("genre_id"),
                description=style_data.get("description"),
                bpm_range=style_data.get("bpm_range"),
                audio_type=style_data.get("audio_type"),
                audio_source=style_data.get("audio_source"),
                reference_url=style_data.get("reference_url"),
                copy_count=style_data.get("copy_count", 0),
            )
            session.add(style)

        await session.commit()
        print(f"Seeded {len(data['data']['styles'])} styles")

    print("Database seeding completed!")


if __name__ == "__main__":
    asyncio.run(seed_database())
