from fastapi import APIRouter

from .endpoints import song

router = APIRouter()
router.include_router(song.router, prefix="/songs", tags=["Songs"])
