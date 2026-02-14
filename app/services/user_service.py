from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.db.db_user import User
from app.models.user import UserCreate, UserUpdate


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    existing = await session.scalar(select(User).where(User.email == user_in.email))
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User.create(name=user_in.name, email=user_in.email, password=user_in.password)

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    return await session.scalar(select(User).where(User.email == email.lower().strip()))


async def get_users(session: AsyncSession, offset: int = 0, limit: int = 100) -> list[User]:
    result = await session.scalars(select(User).offset(offset).limit(limit))
    return list(result.all())


async def update_user(session: AsyncSession, user_id: int, user_in: UserUpdate) -> User:
    user = await get_user_by_id(session, user_id)

    if user_in.email:
        existing = await session.scalar(
            select(User).where(User.email == user_in.email, User.id != user_id)
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

    user.patch_user(
        name=user_in.name,
        email=user_in.email  
    )

    await session.commit()
    await session.refresh(user)

    return user


async def delete_user(session: AsyncSession, user_id: int) -> None:
    user = await get_user_by_id(session, user_id)

    await session.delete(user)
    await session.commit()
