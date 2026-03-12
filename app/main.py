from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

from app.api.routes.prices import router as prices_router
from app.core.config import settings
from app.db.init_db import init_db


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as error:
        logger.warning("Database is not available on startup: %s", error)
    yield


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

app.include_router(prices_router)


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}