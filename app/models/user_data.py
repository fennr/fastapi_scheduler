from typing import Optional

from sqlmodel import JSON, Column, Field, Relationship, SQLModel

from app.models.user import User


class UserDataBase(SQLModel):
    user_id: int = Field(primary_key=True, foreign_key=('user.id'))
    core_id: Optional[int] = Field(primary_key=True, default=None)
    data: dict = Field(default={}, sa_column=Column(JSON))
    user: Optional[User] = Relationship(back_populates='data')


class UserDataCreate(UserDataBase):
    ...


class UserData(UserDataBase, table=True):
    ...
    # id: int = Field(default=None, primary_key=True)


class UserDataRead(UserData):
    ...


class UserDataUpdate(SQLModel):
    data: dict = Field(default={}, sa_column=Column(JSON))
