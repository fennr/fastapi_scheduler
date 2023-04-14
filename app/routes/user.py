from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.db import get_session
from app.models.user import User, UserCreate, UserRead, UserUpdate

router = APIRouter()


async def get_user_by_id(
    user_id: int, session: AsyncSession = Depends(get_session)
) -> User:
    user = await crud.user.get(session=session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id "{user_id}" not found',
        )
    return user


@router.get('/', response_model=list[UserRead])
async def get_users(
    session: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = 100,
) -> list[User]:
    return await crud.user.get_batch(session, limit=limit, offset=offset)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def create_user(
    *,
    session: AsyncSession = Depends(get_session),
    user: UserCreate,
) -> User:
    return await crud.user.create(session, obj=user)


@router.get(
    '/{user_id}', status_code=status.HTTP_200_OK, response_model=UserRead
)
async def get_user(user: User = Depends(get_user_by_id)):
    return user


@router.put(
    '/{user_id}', status_code=status.HTTP_201_CREATED, response_model=UserRead
)
async def update_user(
    *,
    user: UserUpdate,
    db_user: User = Depends(get_user_by_id),
    session: AsyncSession = Depends(get_session),
) -> User:
    return await crud.user.update(session, db_obj=db_user, obj=user)


@router.delete('/{user_id}', response_model=UserRead)
async def delete_user(
    *,
    session: AsyncSession = Depends(get_session),
    user_id: int,
) -> User:
    user = await crud.user.delete(session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id "{user_id}" not found',
        )
    return user
