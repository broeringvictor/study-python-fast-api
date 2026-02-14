from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.utils.typings import Password


class BaseUser(BaseModel):
    name: str
    email: EmailStr


class UserCreate(BaseUser):
    password: Password


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class UserPublic(BaseUser):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserList(BaseModel):
    users: list[UserPublic]
