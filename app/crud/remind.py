from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.remind import Remind, RemindCreate, RemindUpdate

from .base import CRUDBase


class CRUDRemind(CRUDBase[Remind, RemindCreate, RemindUpdate]):
    async def get_task_reminds(
        self,
        *,
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
        task_id: int,
    ) -> list[Remind]:
        statement = (
            select(self.model)
            .limit(limit)
            .offset(offset)
            .where(Remind.task_id == task_id)
        )
        result = await session.execute(statement)
        return result.scalars().all()


remind = CRUDRemind(Remind)
