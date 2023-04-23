from sqlmodel import JSON, Column, Field, SQLModel


class UserDataBase(SQLModel):
    user_id: int = Field(primary_key=True, foreign_key=('user.id'))
    core_id: str = Field(primary_key=True, default=None)
    data: dict = Field(default={}, sa_column=Column(JSON))


class UserDataCreate(UserDataBase):
    ...


class UserData(UserDataBase, table=True):
    ...


class UserDataRead(UserData):
    ...


class UserDataUpdate(SQLModel):
    data: dict = Field(default={}, sa_column=Column(JSON))
