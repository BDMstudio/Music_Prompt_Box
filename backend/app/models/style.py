# File: backend/app/models/style.py

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
import json
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.genre import Genre
    from app.models.folder import FolderStyle


class Style(Base):
    __tablename__ = "styles"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    tags_json: Mapped[str] = mapped_column(Text, nullable=False)
    genre_id: Mapped[Optional[str]] = mapped_column(
        String(50),
        ForeignKey("genres.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    bpm_range: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    audio_type: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    audio_source: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reference_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    copy_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    genre: Mapped[Optional["Genre"]] = relationship("Genre", back_populates="styles")
    folder_associations: Mapped[List["FolderStyle"]] = relationship(
        "FolderStyle", back_populates="style", cascade="all, delete-orphan"
    )

    @property
    def tags(self) -> List[str]:
        return json.loads(self.tags_json) if self.tags_json else []

    @tags.setter
    def tags(self, value: List[str]):
        self.tags_json = json.dumps(value, ensure_ascii=False)
