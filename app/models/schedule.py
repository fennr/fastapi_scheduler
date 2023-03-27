from datetime import datetime
from typing import Optional

from sqlmodel import TIMESTAMP, Column, Field, SQLModel, func


class ScheduleBase(SQLModel):
    trainer: str = Field(index=True, title='Тренер')
    dance: str = Field(index=True, title='Вид танца')
    dtime: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            default=datetime.now(),
            server_default=func.now(),
        )
    )


class Schedule(ScheduleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleRead(Schedule):
    pass


class ScheduleUpdate(SQLModel):
    trainer: Optional[str] = Field(index=True)
    dance: Optional[str] = Field(index=True)
    dtime: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            default=datetime.now(),
            server_default=func.now(),
        )
    )
