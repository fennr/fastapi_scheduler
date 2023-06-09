from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.task import Task, TaskCreate, TaskUpdate

from .base import CRUDBase


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    async def get_by_user(
        self,
        *,
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
        user_id: int,
    ) -> list[Task]:
        statement = (
            select(self.model)
            .limit(limit)
            .offset(offset)
            .where(Task.user_id == user_id)
        )
        result = await session.execute(statement)
        return result.scalars().all()


task = CRUDTask(Task)
