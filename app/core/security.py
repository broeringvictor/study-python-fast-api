from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from app.core.config import config

from jwt import encode


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=config.token_expire_minutes
    )

    to_encode.update({"exp": expire})

    encoded_jwt = encode(to_encode, config.jwt_key, algorithm=config.algorithm)

    return encoded_jwt
