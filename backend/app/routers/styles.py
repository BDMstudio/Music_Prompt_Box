# File: backend/app/routers/styles.py

import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database import get_db
from app.models import Genre, Style, FolderStyle
from app.schemas import StyleCreate, StyleUpdate, StyleResponse, StyleListResponse
from app.config import settings

router = APIRouter(prefix="/api/styles", tags=["styles"])


def get_all_descendant_genre_ids(genre: Genre) -> List[str]:
    ids = [genre.id]
    for child in genre.children:
        ids.extend(get_all_descendant_genre_ids(child))
    return ids


@router.get("", response_model=StyleListResponse)
async def get_styles(
    genre_id: Optional[str] = None,
    search: Optional[str] = None,
    folder_id: Optional[str] = None,
    page: int = Query(1, ge=1),
    size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    db: AsyncSession = Depends(get_db),
):
    query = select(Style).options(joinedload(Style.genre))

    if genre_id:
        genre_result = await db.execute(
            select(Genre)
            .options(joinedload(Genre.children).joinedload(Genre.children))
            .where(Genre.id == genre_id)
        )
        genre = genre_result.unique().scalar_one_or_none()
        if genre:
            descendant_ids = get_all_descendant_genre_ids(genre)
            query = query.where(Style.genre_id.in_(descendant_ids))

    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                Style.name.ilike(search_pattern),
                Style.tags_json.ilike(search_pattern),
                Style.description.ilike(search_pattern),
                Style.bpm_range.ilike(search_pattern),
            )
        )

    if folder_id:
        subq = select(FolderStyle.style_id).where(FolderStyle.folder_id == folder_id)
        query = query.where(Style.id.in_(subq))

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = (
        query.order_by(Style.created_at.desc()).offset((page - 1) * size).limit(size)
    )
    result = await db.execute(query)
    styles = result.unique().scalars().all()

    items = []
    for style in styles:
        folder_check = await db.execute(
            select(FolderStyle).where(FolderStyle.style_id == style.id).limit(1)
        )
        is_favorited = folder_check.scalar_one_or_none() is not None

        items.append(
            StyleResponse(
                id=style.id,
                name=style.name,
                tags=style.tags,
                genre_id=style.genre_id,
                genre_name=style.genre.name if style.genre else None,
                description=style.description,
                bpm_range=style.bpm_range,
                audio_type=style.audio_type,
                audio_source=style.audio_source,
                reference_url=style.reference_url,
                copy_count=style.copy_count,
                is_favorited=is_favorited,
                created_at=style.created_at,
                updated_at=style.updated_at,
            )
        )

    return StyleListResponse(total=total, page=page, size=size, items=items)


@router.get("/{style_id}", response_model=StyleResponse)
async def get_style(style_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Style).options(joinedload(Style.genre)).where(Style.id == style_id)
    )
    style = result.unique().scalar_one_or_none()
    if not style:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Style not found"
        )

    folder_check = await db.execute(
        select(FolderStyle).where(FolderStyle.style_id == style.id).limit(1)
    )
    is_favorited = folder_check.scalar_one_or_none() is not None

    return StyleResponse(
        id=style.id,
        name=style.name,
        tags=style.tags,
        genre_id=style.genre_id,
        genre_name=style.genre.name if style.genre else None,
        description=style.description,
        bpm_range=style.bpm_range,
        audio_type=style.audio_type,
        audio_source=style.audio_source,
        reference_url=style.reference_url,
        copy_count=style.copy_count,
        is_favorited=is_favorited,
        created_at=style.created_at,
        updated_at=style.updated_at,
    )


@router.post("", response_model=StyleResponse, status_code=status.HTTP_201_CREATED)
async def create_style(data: StyleCreate, db: AsyncSession = Depends(get_db)):
    style = Style(
        id=f"style_{uuid.uuid4().hex[:8]}",
        name=data.name,
        tags_json="[]",
        genre_id=data.genre_id,
        description=data.description,
        bpm_range=data.bpm_range,
        audio_type=data.audio_type,
        audio_source=data.audio_source,
        reference_url=data.reference_url,
    )
    style.tags = data.tags

    db.add(style)
    await db.flush()
    await db.refresh(style)

    return StyleResponse(
        id=style.id,
        name=style.name,
        tags=style.tags,
        genre_id=style.genre_id,
        genre_name=None,
        description=style.description,
        bpm_range=style.bpm_range,
        audio_type=style.audio_type,
        audio_source=style.audio_source,
        reference_url=style.reference_url,
        copy_count=style.copy_count,
        is_favorited=False,
        created_at=style.created_at,
        updated_at=style.updated_at,
    )


@router.put("/{style_id}", response_model=StyleResponse)
async def update_style(
    style_id: str, data: StyleUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Style).options(joinedload(Style.genre)).where(Style.id == style_id)
    )
    style = result.unique().scalar_one_or_none()
    if not style:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Style not found"
        )

    update_data = data.model_dump(exclude_unset=True)
    if "tags" in update_data:
        style.tags = update_data.pop("tags")

    for key, value in update_data.items():
        setattr(style, key, value)

    await db.flush()
    await db.refresh(style)

    folder_check = await db.execute(
        select(FolderStyle).where(FolderStyle.style_id == style.id).limit(1)
    )
    is_favorited = folder_check.scalar_one_or_none() is not None

    return StyleResponse(
        id=style.id,
        name=style.name,
        tags=style.tags,
        genre_id=style.genre_id,
        genre_name=style.genre.name if style.genre else None,
        description=style.description,
        bpm_range=style.bpm_range,
        audio_type=style.audio_type,
        audio_source=style.audio_source,
        reference_url=style.reference_url,
        copy_count=style.copy_count,
        is_favorited=is_favorited,
        created_at=style.created_at,
        updated_at=style.updated_at,
    )


@router.delete("/{style_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_style(style_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Style).where(Style.id == style_id))
    style = result.scalar_one_or_none()
    if not style:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Style not found"
        )

    await db.delete(style)


@router.post("/{style_id}/copy", status_code=status.HTTP_204_NO_CONTENT)
async def increment_style_copy_count(style_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Style).where(Style.id == style_id))
    style = result.scalar_one_or_none()
    if not style:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Style not found"
        )

    style.copy_count += 1
