# File: backend/app/routers/__init__.py

from app.routers.genres import router as genres_router
from app.routers.styles import router as styles_router
from app.routers.folders import router as folders_router
from app.routers.tags import router as tags_router
from app.routers.data import router as data_router

__all__ = [
    "genres_router",
    "styles_router",
    "folders_router",
    "tags_router",
    "data_router",
]
