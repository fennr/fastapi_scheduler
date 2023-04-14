from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.db import get_session
from app.models.remind import Remind

router = APIRouter()


async def get_remind_by_id(
    remind_id: int, session: AsyncSession = Depends(get_session)
) -> Remind:
    remind = await crud.remind.get(session=session, id=remind_id)
    if not remind:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Task with id "{remind_id} not found',
        )
    return remind


@router.get('/', response_model=list[Remind])
async def get_reminds(
    session: AsyncSession = Depends(get_session),
    task_id: int = 0,
    offset: int = 0,
    limit: int = 100,
) -> list[Remind]:
    if task_id:
        return await crud.remind.get_task_reminds(
            session=session, task_id=task_id, limit=limit, offset=offset
        )
    return await crud.remind.get_batch(session, limit=limit, offset=offset)


@router.get(
    '/{remind_id}', status_code=status.HTTP_200_OK, response_model=Remind
)
async def get_remind(remind: Remind = Depends(get_remind_by_id)) -> Remind:
    return remind
