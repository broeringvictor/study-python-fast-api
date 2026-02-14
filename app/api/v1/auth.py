from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_context import get_session
from app.db.db_user import User
from app.models.user import UserLogin, UserPublic
from app.core.config import config
from app.core.security import COOKIE_NAME, create_access_token, get_current_user
from app.services.user_service import authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=UserPublic)
async def login(
    user_in: UserLogin,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(session, user_in.email, user_in.password)

    token = create_access_token(data={"sub": user.id})

    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        max_age=config.token_expire_minutes * 60,
        httponly=True,
        samesite="lax",
        secure=not config.debug,
    )

    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key=COOKIE_NAME, httponly=True, samesite="lax")
    return {"message": "Logged out"}


@router.get("/me", response_model=UserPublic)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
