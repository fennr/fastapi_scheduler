
from app.models.user import User, UserBase
from app.models.user_data import UserDataCreate
from tests.data import USERS


def create_user(_data: dict):
    return User(**_data)


def test_create_user():
    user = create_user(USERS['good_user'])
    assert isinstance(user, UserBase)

    user2 = create_user(USERS['minimum_user'])
    assert isinstance(user2, UserBase)


def test_create_user_data():
    user: User = create_user(USERS['good_user'])
    data = UserDataCreate(user_id=user.id, core_id=1, data={'x': 'test'})
    assert isinstance(data, UserDataCreate)
