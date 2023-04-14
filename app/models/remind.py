from datetime import datetime

from sqlmodel import Field, SQLModel

from app.models.utils import get_sa_column


class RemindBase(SQLModel):
    task_id: int = Field(foreign_key='task.id')
    connector: str = Field(default='tg', title='Коннектор для отправки')
    dtime: datetime = Field(sa_column=get_sa_column())
    created_at: datetime = Field(sa_column=get_sa_column())


class RemindCreate(RemindBase):
    ...


class Remind(RemindBase, table=True):
    id: int = Field(default=None, primary_key=True)


class RemindRead(Remind):
    ...


class RemindUpdate(SQLModel):
    dtime: datetime = Field(sa_column=get_sa_column())
