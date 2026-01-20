# File: backend/app/routers/genres.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Genre
from app.schemas import GenreCreate, GenreUpdate, GenreResponse, GenreTreeResponse

router = APIRouter(prefix="/api/genres", tags=["genres"])


@router.get("", response_model=List[GenreTreeResponse])
async def get_genres_tree(db: AsyncSession = Depends(get_db)):
    query = (
        select(Genre)
        .where(Genre.parent_id.is_(None))
        .options(selectinload(Genre.children).selectinload(Genre.children))
        .order_by(Genre.sort_order)
    )
    result = await db.execute(query)
    root_genres = result.scalars().all()
    return [build_genre_tree(g) for g in root_genres]


def build_genre_tree(genre: Genre) -> GenreTreeResponse:
    return GenreTreeResponse(
        id=genre.id,
        name=genre.name,
        parent_id=genre.parent_id,
        level=genre.level,
        sort_order=genre.sort_order,
        description=genre.description,
        era_prompt=genre.era_prompt,
        created_at=genre.created_at,
        updated_at=genre.updated_at,
        children=[
            build_genre_tree(c)
            for c in sorted(genre.children, key=lambda x: x.sort_order)
        ],
    )


@router.get("/{genre_id}", response_model=GenreResponse)
async def get_genre(genre_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Genre).where(Genre.id == genre_id))
    genre = result.scalar_one_or_none()
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found"
        )
    return genre


@router.post("", response_model=GenreResponse, status_code=status.HTTP_201_CREATED)
async def create_genre(data: GenreCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Genre).where(Genre.id == data.id))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Genre ID already exists"
        )

    if data.parent_id:
        parent = await db.execute(select(Genre).where(Genre.id == data.parent_id))
        if not parent.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Parent genre not found"
            )

    genre = Genre(**data.model_dump())
    db.add(genre)
    await db.flush()
    await db.refresh(genre)
    return genre


@router.put("/{genre_id}", response_model=GenreResponse)
async def update_genre(
    genre_id: str, data: GenreUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Genre).where(Genre.id == genre_id))
    genre = result.scalar_one_or_none()
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found"
        )

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(genre, key, value)

    await db.flush()
    await db.refresh(genre)
    return genre


@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre(genre_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Genre).where(Genre.id == genre_id))
    genre = result.scalar_one_or_none()
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found"
        )

    await db.delete(genre)
