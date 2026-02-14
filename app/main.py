from fastapi import FastAPI

from app.core.config import config
from app.api.v1.users import router as users_router

app = FastAPI(title=config.app_name)

app.include_router(users_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}
