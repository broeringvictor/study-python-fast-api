from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_context import get_session
from app.models.user import UserCreate, UserUpdate, UserPublic, UserList
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    return await user_service.create_user(session, user_in)


@router.get("/", response_model=UserList)
async def list_users(
    offset: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
):
    users = await user_service.get_users(session, offset=offset, limit=limit)
    return {"users": users}


@router.get("/{user_id}", response_model=UserPublic)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await user_service.get_user_by_id(session, user_id)


@router.patch("/{user_id}", response_model=UserPublic)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    session: AsyncSession = Depends(get_session),
):
    return await user_service.update_user(session, user_id, user_in)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    await user_service.delete_user(session, user_id)
