from typing import Optional

from sqlmodel import Field, SQLModel


class SongBase(SQLModel):
    name: str = Field(index=True)
    artist: str = Field(index=True)
    year: Optional[int] = None


class Song(SongBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class SongCreate(SongBase):
    pass


class SongRead(SongBase):
    id: int


class SongUpdate(SQLModel):
    name: Optional[str] = None
    artist: Optional[str] = None
    year: Optional[str] = None
