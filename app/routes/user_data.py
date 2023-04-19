from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel.sql.expression import select

from app import crud
from app.db import get_session
from app.exceptions import UserDataNotFound
from app.models.user_data import (UserData, UserDataCreate, UserDataRead,
                                  UserDataUpdate)
from app.routes.user import get_user_by_id

router = APIRouter()


async def user_datas(
    user_id: int, core_id: str, session: AsyncSession = Depends(get_session)
) -> UserData:
    await crud.user.get(session=session, id=user_id)
    statement = (
        select(UserData)
        .where(UserData.user_id == user_id)
        .where(UserData.core_id == core_id)
    )
    result = await session.execute(statement)
    try:
        user_data = result.scalars().one()
    except NoResultFound:
        raise UserDataNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Data with User={user_id} and core_id={core_id} not found',
        )
    return user_data


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=UserDataRead
)
async def create_user_data(
    *,
    session: AsyncSession = Depends(get_session),
    user_data: UserDataCreate,
) -> UserData:
    await get_user_by_id(user_id=user_data.user_id, session=session)
    return await crud.user_data.create(session, obj=user_data)


@router.put('/{user_id}', status_code=201, response_model=UserDataRead)
async def update_user_data(
    *,
    session: AsyncSession = Depends(get_session),
    user_data: UserDataUpdate,
    db_user_data: UserData = Depends(user_datas),
) -> UserData:
    user_data.data = {**db_user_data.data, **user_data.data}
    return await crud.user_data.update(
        session, db_obj=db_user_data, obj=user_data
    )


@router.get(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
)
async def get_user_data(
    core_id: int, user_data: UserDataRead = Depends(user_datas)
) -> UserDataRead:
    return user_data
