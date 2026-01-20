# File: backend/app/routers/tags.py

from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import TagStat
from app.schemas import TagStatResponse, TagCopyRequest

router = APIRouter(prefix="/api/tags", tags=["tags"])


@router.get("/hot", response_model=List[TagStatResponse])
async def get_hot_tags(
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(TagStat)
        .where(TagStat.copy_count > 0)
        .order_by(TagStat.copy_count.desc())
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/copy", status_code=204)
async def record_tag_copies(data: TagCopyRequest, db: AsyncSession = Depends(get_db)):
    for tag in data.tags:
        tag_lower = tag.lower().strip()
        if not tag_lower:
            continue

        result = await db.execute(select(TagStat).where(TagStat.tag == tag_lower))
        tag_stat = result.scalar_one_or_none()

        if tag_stat:
            tag_stat.copy_count += 1
            tag_stat.last_copied_at = datetime.utcnow()
        else:
            tag_stat = TagStat(
                tag=tag_lower,
                copy_count=1,
                last_copied_at=datetime.utcnow(),
            )
            db.add(tag_stat)
