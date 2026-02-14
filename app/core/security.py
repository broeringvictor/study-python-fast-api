from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode, decode, InvalidTokenError
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import config
from app.db.db_context import get_session

COOKIE_NAME = "access_token"


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=config.token_expire_minutes
    )

    to_encode.update({"exp": expire})

    return encode(to_encode, config.jwt_key, algorithm=config.algorithm)


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    from app.services.user_service import get_user_by_id

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise credentials_exception

    try:
        payload = decode(token, config.jwt_key, algorithms=[config.algorithm])
        user_id: int | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = await get_user_by_id(session, user_id)
    return user
