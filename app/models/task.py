from datetime import datetime

from sqlmodel import Field, SQLModel

from app.models.utils import get_sa_column


class TaskBase(SQLModel):
    description: str = Field(
        index=True, nullable=False, title='Описание события'
    )
    place: str | None = Field(title='Место проведения')
    dtime: datetime = Field(sa_column=get_sa_column())
    user_id: int = Field(foreign_key='user.id')
    # user: User = Relationship(back_populates='tasks')
    created_at: datetime = Field(sa_column=get_sa_column())


class TaskCreate(TaskBase):
    ...


class Task(TaskBase, table=True):
    id: int = Field(default=None, primary_key=True)


class TaskRead(Task):
    ...


class TaskUpdate(SQLModel):
    description: str | None = Field(index=True)
    place: str | None = Field(title='Место проведения')
    dtime: datetime | None = Field(sa_column=get_sa_column())
