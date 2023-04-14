from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.db import get_session
from app.models.task import Task, TaskCreate, TaskRead, TaskUpdate

router = APIRouter()


async def get_task_by_id(
    task_id: int, session: AsyncSession = Depends(get_session)
) -> Task:
    task = await crud.task.get(session=session, id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Task with id "{task_id}" not found',
        )
    return task


async def init_task(
    task_obj: TaskCreate, session=Depends(get_session)
) -> Task:
    try:
        task = await crud.task.create(session, obj=task_obj)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id "{task_obj.user_id}" not found',
        )
    return task


@router.get('/', response_model=list[TaskRead])
async def get_tasks(
    session: AsyncSession = Depends(get_session),
    user_id: int = 0,
    offset: int = 0,
    limit: int = 100,
) -> list[Task]:
    if user_id:
        return await crud.task.get_by_user(
            session=session, limit=limit, offset=offset, user_id=user_id
        )
    return await crud.task.get_batch(session, limit=limit, offset=offset)


@router.get('/{task_id}', status_code=status.HTTP_200_OK, response_model=Task)
async def get_task(task: Task = Depends(get_task_by_id)) -> Task:
    return task


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=TaskRead)
async def create_task(task=Depends(init_task)) -> Task:
    return task


@router.put(
    '/{task_id}', status_code=status.HTTP_201_CREATED, response_model=TaskRead
)
async def update_task(
    *,
    task: TaskUpdate,
    db_task: Task = Depends(get_task_by_id),
    session: AsyncSession = Depends(get_session),
) -> Task:
    return await crud.task.update(session, db_obj=db_task, obj=task)


@router.delete('/{task_id}', response_model=TaskRead)
async def delete_task(
    *,
    session: AsyncSession = Depends(get_session),
    task_id: int,
) -> Task:
    task = await crud.task.delete(session, id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Task with id "{task_id}" not found',
        )
    return task
