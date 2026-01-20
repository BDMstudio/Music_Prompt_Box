# File: backend/app/models/tag_stat.py

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TagStat(Base):
    __tablename__ = "tag_stats"

    tag: Mapped[str] = mapped_column(String(100), primary_key=True)
    copy_count: Mapped[int] = mapped_column(Integer, default=0, index=True)
    last_copied_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
