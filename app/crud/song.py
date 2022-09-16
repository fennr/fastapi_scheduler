from ..models.song import Song, SongCreate, SongUpdate
from .base import CRUDBase

song = CRUDBase[Song, SongCreate, SongUpdate](Song)
