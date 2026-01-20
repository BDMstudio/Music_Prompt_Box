# File: backend/app/models/folder.py

from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.style import Style


class Folder(Base):
    __tablename__ = "folders"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    style_associations: Mapped[List["FolderStyle"]] = relationship(
        "FolderStyle", back_populates="folder", cascade="all, delete-orphan"
    )

    @property
    def styles(self) -> List["Style"]:
        return [assoc.style for assoc in self.style_associations]


class FolderStyle(Base):
    __tablename__ = "folder_styles"

    folder_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("folders.id", ondelete="CASCADE"), primary_key=True
    )
    style_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("styles.id", ondelete="CASCADE"), primary_key=True
    )
    added_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    folder: Mapped["Folder"] = relationship(
        "Folder", back_populates="style_associations"
    )
    style: Mapped["Style"] = relationship("Style", back_populates="folder_associations")
