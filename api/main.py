from contextlib import asynccontextmanager
from typing import AsyncGenerator
import redis.asyncio as aioredis
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from api.core.config import get_settings
settings = get_settings() #do poprawki, przenies funkcje na cos w stylu def create_app() -> FastAPI:, wtedy nie bedzie potrzeby na globalke 
@asynccontextmanager
async def lifespan(app:FastAPI) -> AsyncGenerator[None, None]:
    settings = get_settings()
    try:
        pool = aioredis.ConnectionPool.from_url(
            settings.redis_url,
            decode_responses = True,
            max_connections = 20
        )

        redis = aioredis.Redis(connection_pool=pool)
        await redis.ping()
        app.state.redis = redis
        app.state.redis_pool = pool

        yield
    finally:
        if hasattr(app.state, "redis"):
            await app.state.redis.aclose()

        if hasattr(app.state, "redis_pool"):
            await app.state.redis_pool.disconnect()


app = FastAPI(
    title="narzedzia.lh.pl",
    version="0.1",
    lifespan=lifespan,
)

#CORS do testu czy w ogole potrzebne w tym przypadku
app.add_middleware (
    CORSMiddleware,
    allow_origins=[settings.cors_origin],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}