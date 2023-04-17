from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.db import get_session
from app.exceptions import RemindNotFound
from app.models.remind import Remind, RemindCreate, RemindUpdate
from app.routes.task import get_task_by_id

router = APIRouter()


async def get_remind_by_id(
    remind_id: int, session: AsyncSession = Depends(get_session)
) -> Remind:
    remind = await crud.remind.get(session=session, id=remind_id)
    if not remind:
        raise RemindNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Task with id "{remind_id} not found',
        )
    return remind


async def init_remind(
    remind_obj: RemindCreate, session=Depends(get_session)
) -> Remind:
    await get_task_by_id(task_id=remind_obj.task_id, session=session)
    remind = await crud.remind.create(session=session, obj=remind_obj)
    return remind


@router.get('/', response_model=list[Remind])
async def get_reminds(
    session: AsyncSession = Depends(get_session),
    task_id: int = 0,
    offset: int = 0,
    limit: int = 100,
) -> list[Remind]:
    if task_id:  # pragma: no cover
        return await crud.remind.get_task_reminds(
            session=session, task_id=task_id, limit=limit, offset=offset
        )
    return await crud.remind.get_batch(session, limit=limit, offset=offset)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Remind)
async def create_remind(remind=Depends(init_remind)) -> Remind:
    return remind


@router.get(
    '/{remind_id}', status_code=status.HTTP_200_OK, response_model=Remind
)
async def get_remind(remind: Remind = Depends(get_remind_by_id)) -> Remind:
    return remind


@router.put(
    '/{remind_id}',
    status_code=status.HTTP_201_CREATED,
    response_model=Remind,
)
async def update_remind(
    *,
    remind: RemindUpdate,
    db_remind: Remind = Depends(get_remind_by_id),
    session: AsyncSession = Depends(get_session),
) -> Remind:
    return await crud.remind.update(session, db_obj=db_remind, obj=remind)


@router.delete('/{remind_id}', response_model=Remind)
async def delete_remind(
    *,
    session: AsyncSession = Depends(get_session),
    remind_id: int,
) -> Remind:
    remind = await crud.remind.delete(session, id=remind_id)
    if not remind:  # pragma: no cover
        raise RemindNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Remind with id={remind_id} not found',
        )
    return remind
