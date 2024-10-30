from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi_cache import FastAPICache

from src.init import redis_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(redis_manager.redis, prefix=['fastapi_cache'])
    yield 
    await redis_manager.close()

app = FastAPI(docs=None, lifespan=lifespan)

from src.routers.auth import router as auth_router
from src.routers.profile import router as profile_router
from src.routers.clients import router as clients_router

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(clients_router)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)