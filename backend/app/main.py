# File: backend/app/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db, close_db
from app.routers import (
    genres_router,
    styles_router,
    folders_router,
    tags_router,
    data_router,
    itunes_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    settings.STORAGE_PATH.mkdir(parents=True, exist_ok=True)
    settings.AUDIO_PATH.mkdir(parents=True, exist_ok=True)
    yield
    await close_db()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(genres_router)
app.include_router(styles_router)
app.include_router(folders_router)
app.include_router(tags_router)
app.include_router(data_router)
app.include_router(itunes_router)

app.mount("/storage", StaticFiles(directory=str(settings.STORAGE_PATH)), name="storage")


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": settings.APP_VERSION}


# Serve production frontend: mount /assets for JS/CSS, catch-all SPA fallback LAST
if settings.FRONTEND_DIST_PATH.exists():
    assets_path = settings.FRONTEND_DIST_PATH / "assets"
    if assets_path.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_path)), name="frontend_assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = settings.FRONTEND_DIST_PATH / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(settings.FRONTEND_DIST_PATH / "index.html")
