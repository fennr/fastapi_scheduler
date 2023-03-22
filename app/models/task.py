from datetime import datetime
from typing import Optional

from sqlmodel import TIMESTAMP, Column, Field, SQLModel, func


class TaskBase(SQLModel):
    user: str = Field(index=True, title='Пользователь')
    description: str = Field(index=True, title='Описание события')
    dtime: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            default=datetime.now(),
            server_default=func.now(),
        )
    )


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class TaskCreate(TaskBase):
    pass


class TaskRead(Task):
    pass


class TaskUpdate(SQLModel):
    user: Optional[str] = Field(index=True)
    description: Optional[str] = Field(index=True)
    dtime: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            default=datetime.now(),
            server_default=func.now(),
        )
    )
