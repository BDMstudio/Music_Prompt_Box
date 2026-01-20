# File: backend/app/schemas/genre.py

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class GenreBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    parent_id: Optional[str] = None
    level: int = Field(default=1, ge=1, le=3)
    sort_order: int = Field(default=0)
    description: Optional[str] = None
    era_prompt: Optional[str] = None


class GenreCreate(GenreBase):
    id: str = Field(..., min_length=1, max_length=50)


class GenreUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    parent_id: Optional[str] = None
    level: Optional[int] = Field(None, ge=1, le=3)
    sort_order: Optional[int] = None
    description: Optional[str] = None
    era_prompt: Optional[str] = None


class GenreResponse(GenreBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GenreTreeResponse(GenreResponse):
    children: List["GenreTreeResponse"] = []
