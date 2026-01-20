# File: backend/app/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db, close_db
from app.routers import (
    genres_router,
    styles_router,
    folders_router,
    tags_router,
    data_router,
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

app.mount("/storage", StaticFiles(directory=str(settings.STORAGE_PATH)), name="storage")


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": settings.APP_VERSION}
