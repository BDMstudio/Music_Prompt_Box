# File: backend/app/models/genre.py

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.style import Style


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    parent_id: Mapped[Optional[str]] = mapped_column(
        String(50), ForeignKey("genres.id", ondelete="CASCADE"), nullable=True
    )
    level: Mapped[int] = mapped_column(Integer, default=1)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    era_prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    parent: Mapped[Optional["Genre"]] = relationship(
        "Genre", remote_side=[id], back_populates="children"
    )
    children: Mapped[List["Genre"]] = relationship(
        "Genre", back_populates="parent", cascade="all, delete-orphan"
    )
    styles: Mapped[List["Style"]] = relationship("Style", back_populates="genre")
