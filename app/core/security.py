from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode, decode, InvalidTokenError
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import config
from app.db.db_context import get_session

COOKIE_NAME = "access_token"
security_scheme = HTTPBearer(auto_error=False)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=config.token_expire_minutes
    )

    to_encode.update({"exp": expire})

    return encode(to_encode, config.jwt_key, algorithm=config.algorithm)


async def get_current_user(
    request: Request,
    token_auth: HTTPAuthorizationCredentials | None = Depends(security_scheme),
    session: AsyncSession = Depends(get_session),
):
    from app.services.user_service import get_user_by_id

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    # 1. Cookie (browser)
    token = request.cookies.get(COOKIE_NAME)

    # 2. Header Authorization: Bearer (Scalar/Postman)
    if not token and token_auth:
        token = token_auth.credentials

    if not token:
        raise credentials_exception

    try:
        payload = decode(token, config.jwt_key, algorithms=[config.algorithm])
        user_id_raw = payload.get("sub")
        if user_id_raw is None:
            raise credentials_exception
        user_id = int(user_id_raw)
    except (InvalidTokenError, ValueError):
        raise credentials_exception

    user = await get_user_by_id(session, user_id)
    return user
