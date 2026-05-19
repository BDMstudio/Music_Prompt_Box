# File: backend/seeds/seed_db.py

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import engine, AsyncSessionLocal, Base
from app.models import Genre, Style, Folder, FolderStyle

from sqlalchemy.dialects.sqlite import insert as sqlite_insert


async def seed_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    seed_file = Path(__file__).parent / "initial_data.json"
    with open(seed_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    async with AsyncSessionLocal() as session:

        # --- Upsert genres ---
        for genre_data in data["data"]["genres"]:
            stmt = sqlite_insert(Genre).values(
                id=genre_data["id"],
                name=genre_data["name"],
                parent_id=genre_data.get("parent_id"),
                level=genre_data.get("level", 1),
                sort_order=genre_data.get("sort_order", 0),
                description=genre_data.get("description"),
                era_prompt=genre_data.get("era_prompt"),
            )
            # On conflict: update all mutable fields
            stmt = stmt.on_conflict_do_update(
                index_elements=["id"],
                set_={
                    "name": stmt.excluded.name,
                    "parent_id": stmt.excluded.parent_id,
                    "level": stmt.excluded.level,
                    "sort_order": stmt.excluded.sort_order,
                    "description": stmt.excluded.description,
                    "era_prompt": stmt.excluded.era_prompt,
                },
            )
            await session.execute(stmt)

        await session.commit()
        print(f"Upserted {len(data['data']['genres'])} genres")

        # --- Upsert styles ---
        for style_data in data["data"]["styles"]:
            audio_metadata = style_data.get("audio_metadata")
            metadata_str = json.dumps(audio_metadata, ensure_ascii=False) if audio_metadata else None

            stmt = sqlite_insert(Style).values(
                id=style_data["id"],
                name=style_data["name"],
                tags_json=json.dumps(style_data.get("tags", []), ensure_ascii=False),
                genre_id=style_data.get("genre_id"),
                description=style_data.get("description"),
                bpm_range=style_data.get("bpm_range"),
                audio_type=style_data.get("audio_type"),
                audio_source=style_data.get("audio_source"),
                audio_platform=style_data.get("audio_platform"),
                audio_metadata=metadata_str,
                reference_url=style_data.get("reference_url"),
                copy_count=style_data.get("copy_count", 0),
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=["id"],
                set_={
                    "name": stmt.excluded.name,
                    "tags_json": stmt.excluded.tags_json,
                    "genre_id": stmt.excluded.genre_id,
                    "description": stmt.excluded.description,
                    "bpm_range": stmt.excluded.bpm_range,
                    "audio_type": stmt.excluded.audio_type,
                    "audio_source": stmt.excluded.audio_source,
                    "audio_platform": stmt.excluded.audio_platform,
                    "audio_metadata": stmt.excluded.audio_metadata,
                    "reference_url": stmt.excluded.reference_url,
                    # copy_count NOT overwritten on upsert — preserve runtime stats
                },
            )
            await session.execute(stmt)

        await session.commit()
        print(f"Upserted {len(data['data']['styles'])} styles")

    print("Database seeding completed!")


if __name__ == "__main__":
    asyncio.run(seed_database())
