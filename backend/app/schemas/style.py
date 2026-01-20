# File: backend/app/schemas/style.py

from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field


class StyleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    tags: List[str] = Field(..., min_length=1)
    genre_id: Optional[str] = None
    description: Optional[str] = None
    bpm_range: Optional[str] = Field(None, max_length=20)
    audio_type: Optional[Literal["local", "url"]] = None
    audio_source: Optional[str] = None
    reference_url: Optional[str] = None


class StyleCreate(StyleBase):
    pass


class StyleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    tags: Optional[List[str]] = Field(None, min_length=1)
    genre_id: Optional[str] = None
    description: Optional[str] = None
    bpm_range: Optional[str] = Field(None, max_length=20)
    audio_type: Optional[Literal["local", "url"]] = None
    audio_source: Optional[str] = None
    reference_url: Optional[str] = None


class StyleResponse(BaseModel):
    id: str
    name: str
    tags: List[str]
    genre_id: Optional[str] = None
    genre_name: Optional[str] = None
    description: Optional[str] = None
    bpm_range: Optional[str] = None
    audio_type: Optional[str] = None
    audio_source: Optional[str] = None
    reference_url: Optional[str] = None
    copy_count: int = 0
    is_favorited: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StyleListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: List[StyleResponse]
