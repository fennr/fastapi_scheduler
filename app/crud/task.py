from app.models.task import Task, TaskCreate, TaskUpdate

from .base import CRUDBase


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    """async def get_by_user(
        self,
        session: AsyncSession,
        *,
        user: str,
    ) -> list[Task]:
        statement = select(self.model).where(Task.user == user)
        result = await session.execute(statement)
        return result.scalars().all()
    """


task = CRUDTask(Task)
