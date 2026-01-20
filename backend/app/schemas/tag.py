# File: backend/app/schemas/tag.py

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class TagStatResponse(BaseModel):
    tag: str
    copy_count: int
    last_copied_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TagCopyRequest(BaseModel):
    tags: List[str]
