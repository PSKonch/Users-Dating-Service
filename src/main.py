from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache

from src.init import redis_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(redis_manager.redis, prefix=['fastapi_cache'])
    yield 
    await redis_manager.close()

app = FastAPI(lifespan=lifespan)