from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.main import api_router

app = FastAPI(
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(router=api_router, prefix=settings.API_V1_STR)
