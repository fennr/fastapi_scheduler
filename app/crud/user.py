from app.models.user import User, UserCreate, UserUpdate

from .base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    ...


user = CRUDUser(User)
