
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app import crud
from app.db import get_session
from app.models.schedule import (Schedule, ScheduleCreate, ScheduleRead,
                                 ScheduleUpdate)

router = APIRouter()

async def get_entry_by_id(
    schedule_id: int, session: AsyncSession = Depends(get_session)
) -> Schedule:
    schedule = await crud.schedule.get(session=session, id=schedule_id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Task with id "{schedule_id}" not found',
        )
    return schedule

async def entry_by_trainer(
    trainer: str, session: AsyncSession = Depends(get_session)
) -> list[Schedule]:
    statement = select(Schedule).where(Schedule.trainer == trainer)
    result = await session.execute(statement)
    return result.scalars().all()

@router.get('/', response_model=list[ScheduleRead])
async def get_schedule(
    session: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = 100,
) -> list[Schedule]:
    return await crud.schedule.get_batch(session, limit=limit, offset=offset)


@router.get('/{trainer}', response_model=list[ScheduleRead])
async def get_trainer_schedule(
    *,
    tasks: list[Schedule] = Depends(entry_by_trainer),
) -> list[Schedule]:
    return tasks


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ScheduleRead)
async def create_schedule(
    *,
    session: AsyncSession = Depends(get_session),
    schedule: ScheduleCreate,
) -> Schedule:
    return await crud.schedule.create(session, obj=schedule)


@router.get(
    '/{schedule_id}', status_code=status.HTTP_200_OK, response_model=ScheduleRead
)
async def get_entry(schedule: Schedule = Depends(get_entry_by_id)):
    return schedule


@router.put(
    '/{schedule_id}', status_code=status.HTTP_201_CREATED, response_model=ScheduleRead
)
async def update_entry(
    *,
    schedule: ScheduleUpdate,
    db_schedule: Schedule = Depends(get_entry_by_id),
    session: AsyncSession = Depends(get_session),
) -> Schedule:
    return await crud.schedule.update(session, db_obj=db_schedule, obj=schedule)


@router.delete('/{schedule_id}', response_model=ScheduleRead)
async def delete_entry(
    *,
    session: AsyncSession = Depends(get_session),
    schedule_id: int,
) -> Schedule:
    schedule = await crud.schedule.delete(session, id=schedule_id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Schedule with id "{schedule_id}" not found',
        )
    return schedule
