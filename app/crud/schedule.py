
from app.models.schedule import Schedule, ScheduleCreate, ScheduleUpdate

from .base import CRUDBase


class CRUDSchedule(CRUDBase[Schedule, ScheduleCreate, ScheduleUpdate]):
    """async def get_by_user(
        self,
        session: AsyncSession,
        *,
        user: str,
    ) -> list[Schedule]:
        statement = select(self.model).where(Schedule.user == user)
        result = await session.execute(statement)
        return result.scalars().all()
    """


schedule = CRUDSchedule(Schedule)
