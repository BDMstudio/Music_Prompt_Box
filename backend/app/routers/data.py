# File: backend/app/routers/data.py

from datetime import datetime
from typing import Optional, Literal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Genre, Style, Folder, FolderStyle

router = APIRouter(prefix="/api/data", tags=["data"])


class ExportData(BaseModel):
    version: str = "1.0"
    exported_at: datetime
    data: dict


class ImportRequest(BaseModel):
    version: str
    exported_at: datetime
    data: dict


@router.get("/export")
async def export_data(
    scope: Literal["all", "genre", "folder"] = "all",
    genre_id: Optional[str] = None,
    folder_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    genres_result = await db.execute(
        select(Genre).options(selectinload(Genre.children)).order_by(Genre.sort_order)
    )
    all_genres = genres_result.scalars().all()

    genres_data = [
        {
            "id": g.id,
            "name": g.name,
            "parent_id": g.parent_id,
            "level": g.level,
            "sort_order": g.sort_order,
            "description": g.description,
            "era_prompt": g.era_prompt,
        }
        for g in all_genres
    ]

    styles_query = select(Style)
    if scope == "genre" and genre_id:
        styles_query = styles_query.where(Style.genre_id == genre_id)
    elif scope == "folder" and folder_id:
        subq = select(FolderStyle.style_id).where(FolderStyle.folder_id == folder_id)
        styles_query = styles_query.where(Style.id.in_(subq))

    styles_result = await db.execute(styles_query)
    styles = styles_result.scalars().all()

    styles_data = [
        {
            "id": s.id,
            "name": s.name,
            "tags": s.tags,
            "genre_id": s.genre_id,
            "description": s.description,
            "bpm_range": s.bpm_range,
            "audio_type": s.audio_type,
            "audio_source": s.audio_source,
            "reference_url": s.reference_url,
            "copy_count": s.copy_count,
        }
        for s in styles
    ]

    folders_result = await db.execute(select(Folder))
    folders = folders_result.scalars().all()

    folders_data = []
    for folder in folders:
        fs_result = await db.execute(
            select(FolderStyle.style_id).where(FolderStyle.folder_id == folder.id)
        )
        style_ids = [row[0] for row in fs_result.all()]
        folders_data.append(
            {
                "id": folder.id,
                "name": folder.name,
                "style_ids": style_ids,
            }
        )

    export = {
        "version": "1.0",
        "exported_at": datetime.utcnow().isoformat(),
        "data": {
            "genres": genres_data,
            "styles": styles_data,
            "folders": folders_data,
        },
    }

    return JSONResponse(content=export)


@router.post("/import")
async def import_data(
    data: ImportRequest,
    mode: Literal["overwrite", "merge"] = Query(...),
    db: AsyncSession = Depends(get_db),
):
    if data.version != "1.0":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported version: {data.version}",
        )

    import_data = data.data

    if mode == "overwrite":
        await db.execute(
            select(FolderStyle).execution_options(synchronize_session="fetch")
        )
        for table in [FolderStyle, Style, Folder, Genre]:
            result = await db.execute(select(table))
            for item in result.scalars().all():
                await db.delete(item)

    genres_imported = 0
    for genre_data in import_data.get("genres", []):
        if mode == "merge":
            existing = await db.execute(
                select(Genre).where(Genre.id == genre_data["id"])
            )
            if existing.scalar_one_or_none():
                continue

        genre = Genre(
            id=genre_data["id"],
            name=genre_data["name"],
            parent_id=genre_data.get("parent_id"),
            level=genre_data.get("level", 1),
            sort_order=genre_data.get("sort_order", 0),
            description=genre_data.get("description"),
            era_prompt=genre_data.get("era_prompt"),
        )
        db.add(genre)
        genres_imported += 1

    await db.flush()

    styles_imported = 0
    for style_data in import_data.get("styles", []):
        if mode == "merge":
            existing = await db.execute(
                select(Style).where(Style.id == style_data["id"])
            )
            if existing.scalar_one_or_none():
                continue

        style = Style(
            id=style_data["id"],
            name=style_data["name"],
            tags_json="[]",
            genre_id=style_data.get("genre_id"),
            description=style_data.get("description"),
            bpm_range=style_data.get("bpm_range"),
            audio_type=style_data.get("audio_type"),
            audio_source=style_data.get("audio_source"),
            reference_url=style_data.get("reference_url"),
            copy_count=style_data.get("copy_count", 0),
        )
        style.tags = style_data.get("tags", [])
        db.add(style)
        styles_imported += 1

    await db.flush()

    folders_imported = 0
    for folder_data in import_data.get("folders", []):
        if mode == "merge":
            existing = await db.execute(
                select(Folder).where(Folder.id == folder_data["id"])
            )
            if existing.scalar_one_or_none():
                continue

        folder = Folder(
            id=folder_data["id"],
            name=folder_data["name"],
        )
        db.add(folder)
        await db.flush()

        for style_id in folder_data.get("style_ids", []):
            style_exists = await db.execute(select(Style).where(Style.id == style_id))
            if style_exists.scalar_one_or_none():
                fs = FolderStyle(folder_id=folder.id, style_id=style_id)
                db.add(fs)

        folders_imported += 1

    return {
        "message": "Import successful",
        "genres_imported": genres_imported,
        "styles_imported": styles_imported,
        "folders_imported": folders_imported,
    }
