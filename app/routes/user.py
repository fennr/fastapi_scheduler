from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.db import get_session
from app.exceptions import UserExist, UserNotFound
from app.models.user import User, UserCreate, UserUpdate

router = APIRouter()


async def get_user_by_id(
    user_id: int, session: AsyncSession = Depends(get_session)
) -> User:
    user = await crud.user.get(session, id=user_id)
    if not user:   # pragma: no cover
        raise UserNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id={user_id} not found',
        )
    return user


async def create_user_if_not_exist(
    user_obj: UserCreate, session=Depends(get_session)
) -> User:
    try:
        return await crud.user.create(session, obj=user_obj)
    except IntegrityError:
        raise UserExist(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already exist',
        )


async def get_exist_user(session, *, obj: UserCreate) -> User | None:
    user_tg = await get_social_user(session, tg=obj.tg)
    user_vk = await get_social_user(session, vk=obj.vk)
    if user_tg:
        return user_tg[0]
    if user_vk:
        return user_vk[0]
    return None


async def get_social_user(
    session=Depends(get_session),
    vk: str | None = None,
    tg: str | None = None,
) -> list[User]:
    if tg:
        return [await crud.user.get_tg_user(session, tg=tg)]
    elif vk:
        return [await crud.user.get_vk_user(session, vk=vk)]
    else:
        return await crud.user.get_batch(session, limit=100, offset=0)


@router.get('/', response_model=list[User])
async def get_users(
    users=Depends(get_social_user),
) -> list[User]:
    return users


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(
    *,
    user: User = Depends(create_user_if_not_exist),
) -> User:
    return user


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=User)
async def get_user(user: User = Depends(get_user_by_id)):
    return user


@router.put(
    '/{user_id}', status_code=status.HTTP_201_CREATED, response_model=User
)
async def update_user(
    *,
    user: UserUpdate,
    db_user: User = Depends(get_user_by_id),
    session: AsyncSession = Depends(get_session),
) -> User:
    return await crud.user.update(session, db_obj=db_user, obj=user)


@router.delete('/{user_id}', response_model=User)
async def delete_user(
    *,
    session: AsyncSession = Depends(get_session),
    user_id: int,
) -> User:
    user = await crud.user.delete(session, id=user_id)
    if not user:  # pragma: no cover
        raise UserNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id "{user_id}" not found',
        )
    return user
