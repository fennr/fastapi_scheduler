from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from app.models.utils import get_sa_column


class UserBase(SQLModel):
    tg: Optional[str] = Field(index=True, unique=True)
    vk: Optional[str] = Field(index=True, unique=True)
    # data: list['UserData'] = Relationship(back_populates='user')
    # tasks: list['Task'] = Relationship(back_populates='user')
    created_at: datetime = Field(sa_column=get_sa_column())


class UserCreate(UserBase):
    ...


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)


class UserRead(User):
    ...


class UserUpdate(SQLModel):
    tg: Optional[str] = Field(index=True, unique=True)
    vk: Optional[str] = Field(index=True, unique=True)
