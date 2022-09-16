from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud  # isort:skip
from app.db import get_session  # isort:skip
from app.models.song import SongCreate, SongRead, SongUpdate  # isort:skip

router = APIRouter()


@router.get("/", response_model=list[SongRead])
async def get_songs(
    session: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = 100,
):
    return await crud.song.get_batch(session, limit=limit, offset=offset)


@router.get("/{song_id}", response_model=SongRead)
async def get_song(
    *,
    session: AsyncSession = Depends(get_session),
    song_id: int,
):
    song = await crud.song.get(session, id=song_id)

    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Song with id {song_id} does not exist in system",
        )

    return song


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SongRead)
async def create_song(
    *,
    session: AsyncSession = Depends(get_session),
    song: SongCreate,
):
    return await crud.song.create(session, obj=song)


@router.patch("/{song_id}", response_model=SongRead)
async def update_song(
    *,
    session: AsyncSession = Depends(get_session),
    song_id: int,
    song: SongUpdate,
):
    db_song = await crud.song.get(session, id=song_id)

    if not db_song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Song with id {song_id} does not exist in system",
        )

    return await crud.song.update(session, db_obj=db_song, obj=song)


@router.delete("/{song_id}", response_model=SongRead)
async def delete_song(
    *,
    session: AsyncSession = Depends(get_session),
    song_id: int,
):
    song = await crud.song.delete(session, id=song_id)

    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Song with id {song_id} does not exist in system",
        )

    return song
