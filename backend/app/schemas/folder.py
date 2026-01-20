# File: backend/app/schemas/folder.py

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class FolderBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class FolderCreate(FolderBase):
    pass


class FolderUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class FolderResponse(FolderBase):
    id: str
    style_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FolderAddStyle(BaseModel):
    style_id: str
