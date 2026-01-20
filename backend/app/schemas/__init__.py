# File: backend/app/schemas/__init__.py

from app.schemas.genre import (
    GenreCreate,
    GenreUpdate,
    GenreResponse,
    GenreTreeResponse,
)
from app.schemas.style import (
    StyleCreate,
    StyleUpdate,
    StyleResponse,
    StyleListResponse,
)
from app.schemas.folder import (
    FolderCreate,
    FolderUpdate,
    FolderResponse,
    FolderAddStyle,
)
from app.schemas.tag import TagStatResponse, TagCopyRequest

__all__ = [
    "GenreCreate",
    "GenreUpdate",
    "GenreResponse",
    "GenreTreeResponse",
    "StyleCreate",
    "StyleUpdate",
    "StyleResponse",
    "StyleListResponse",
    "FolderCreate",
    "FolderUpdate",
    "FolderResponse",
    "FolderAddStyle",
    "TagStatResponse",
    "TagCopyRequest",
]
