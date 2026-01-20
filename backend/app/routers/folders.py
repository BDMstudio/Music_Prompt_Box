# File: backend/app/routers/folders.py

import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Folder, FolderStyle, Style
from app.schemas import FolderCreate, FolderUpdate, FolderResponse, FolderAddStyle

router = APIRouter(prefix="/api/folders", tags=["folders"])


@router.get("", response_model=List[FolderResponse])
async def get_folders(db: AsyncSession = Depends(get_db)):
    query = select(Folder).order_by(Folder.created_at)
    result = await db.execute(query)
    folders = result.scalars().all()

    items = []
    for folder in folders:
        count_query = (
            select(func.count())
            .select_from(FolderStyle)
            .where(FolderStyle.folder_id == folder.id)
        )
        count_result = await db.execute(count_query)
        style_count = count_result.scalar() or 0

        items.append(
            FolderResponse(
                id=folder.id,
                name=folder.name,
                style_count=style_count,
                created_at=folder.created_at,
                updated_at=folder.updated_at,
            )
        )

    return items


@router.get("/{folder_id}", response_model=FolderResponse)
async def get_folder(folder_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Folder).where(Folder.id == folder_id))
    folder = result.scalar_one_or_none()
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found"
        )

    count_query = (
        select(func.count())
        .select_from(FolderStyle)
        .where(FolderStyle.folder_id == folder.id)
    )
    count_result = await db.execute(count_query)
    style_count = count_result.scalar() or 0

    return FolderResponse(
        id=folder.id,
        name=folder.name,
        style_count=style_count,
        created_at=folder.created_at,
        updated_at=folder.updated_at,
    )


@router.post("", response_model=FolderResponse, status_code=status.HTTP_201_CREATED)
async def create_folder(data: FolderCreate, db: AsyncSession = Depends(get_db)):
    folder = Folder(
        id=f"folder_{uuid.uuid4().hex[:8]}",
        name=data.name,
    )
    db.add(folder)
    await db.flush()
    await db.refresh(folder)

    return FolderResponse(
        id=folder.id,
        name=folder.name,
        style_count=0,
        created_at=folder.created_at,
        updated_at=folder.updated_at,
    )


@router.put("/{folder_id}", response_model=FolderResponse)
async def update_folder(
    folder_id: str, data: FolderUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Folder).where(Folder.id == folder_id))
    folder = result.scalar_one_or_none()
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found"
        )

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(folder, key, value)

    await db.flush()
    await db.refresh(folder)

    count_query = (
        select(func.count())
        .select_from(FolderStyle)
        .where(FolderStyle.folder_id == folder.id)
    )
    count_result = await db.execute(count_query)
    style_count = count_result.scalar() or 0

    return FolderResponse(
        id=folder.id,
        name=folder.name,
        style_count=style_count,
        created_at=folder.created_at,
        updated_at=folder.updated_at,
    )


@router.delete("/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_folder(folder_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Folder).where(Folder.id == folder_id))
    folder = result.scalar_one_or_none()
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found"
        )

    await db.delete(folder)


@router.post("/{folder_id}/styles", status_code=status.HTTP_201_CREATED)
async def add_style_to_folder(
    folder_id: str, data: FolderAddStyle, db: AsyncSession = Depends(get_db)
):
    folder_result = await db.execute(select(Folder).where(Folder.id == folder_id))
    if not folder_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found"
        )

    style_result = await db.execute(select(Style).where(Style.id == data.style_id))
    if not style_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Style not found"
        )

    existing = await db.execute(
        select(FolderStyle).where(
            FolderStyle.folder_id == folder_id,
            FolderStyle.style_id == data.style_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Style already in folder"
        )

    folder_style = FolderStyle(folder_id=folder_id, style_id=data.style_id)
    db.add(folder_style)


@router.delete("/{folder_id}/styles/{style_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_style_from_folder(
    folder_id: str, style_id: str, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(FolderStyle).where(
            FolderStyle.folder_id == folder_id,
            FolderStyle.style_id == style_id,
        )
    )
    folder_style = result.scalar_one_or_none()
    if not folder_style:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Style not in folder"
        )

    await db.delete(folder_style)
