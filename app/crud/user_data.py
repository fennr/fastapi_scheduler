from app.models.user_data import UserData, UserDataCreate, UserDataUpdate

from .base import CRUDBase


class CRUDUserData(CRUDBase[UserData, UserDataCreate, UserDataUpdate]):
    ...


user_data = CRUDUserData(UserData)
