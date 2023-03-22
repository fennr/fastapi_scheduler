from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

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


async def user_tasks(
    username: str, session: AsyncSession = Depends(get_session)
) -> list[Task]:
    statement = select(Task).where(Task.user == username)
    result = await session.execute(statement)
    return result.scalars().all()


@router.get('/', response_model=list[TaskRead])
async def get_tasks(
    session: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = 100,
) -> list[Task]:
    return await crud.task.get_batch(session, limit=limit, offset=offset)


@router.get('/{username}', response_model=list[TaskRead])
async def get_user_tasks(
    *,
    tasks: list[Task] = Depends(user_tasks),
) -> list[Task]:
    return tasks


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=TaskRead)
async def create_task(
    *,
    session: AsyncSession = Depends(get_session),
    task: TaskCreate,
) -> Task:
    return await crud.task.create(session, obj=task)


@router.get(
    '/{task_id}', status_code=status.HTTP_200_OK, response_model=TaskRead
)
async def get_task(task: Task = Depends(get_task_by_id)):
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
