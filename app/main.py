from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.core.config import config
from app.api.v1.users import router as users_router
from app.api.v1.auth import router as auth_router

app = FastAPI(title=config.app_name, docs_url=None, redoc_url=None)

app.include_router(users_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")


@app.get("/docs", include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=config.app_name,
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}
