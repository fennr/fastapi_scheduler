import pytest
from httpx import AsyncClient

from app.exceptions import UserDataNotFound, UserException
from app.models.user import User
from app.models.user_data import UserData
from app.routes.user_data import user_datas
from tests.data import USERS

CORE_ID = '123'


async def create_user(
    client: AsyncClient, user_json: dict = USERS['good_user']
) -> User:
    r = await client.post('/user/', json=user_json)
    return User(**r.json())


async def create_user_data(
    client, user_id: int, user_data_json: dict = {'test': 123}
) -> UserData:
    data = {
        'user_id': user_id,
        'core_id': CORE_ID,
        'data': user_data_json,
    }
    r = await client.post('/user_data/', json=data)
    if r.status_code not in [200, 201]:
        raise UserException(status_code=404, detail='Test error')
    return UserData(**r.json())


async def test_create_user_data(client):
    user = await create_user(client)
    user_data = await create_user_data(client, user.id, {'x': 1})
    assert user_data.data['x'] == 1


async def test_create_with_bad_user(client):
    fake_user_id = 0
    with pytest.raises(UserException) as exc_info:
        await create_user_data(client, fake_user_id, {'x': 1})
    assert exc_info.value.status_code == 404


async def test_get_user_data(client, session):
    user = await create_user(client)
    user_data_db = await create_user_data(client, user.id, {'x': 1})
    # проверка функции Depends
    user_data = await user_datas(user.id, CORE_ID, session)
    assert user_data == user_data_db
    # проверка API
    r = await client.get(f'/user_data/{user.id}?core_id={CORE_ID}')
    user_data = UserData(**r.json())
    assert user_data == user_data_db


async def test_get_user_data_not_found(client, session):
    user = await create_user(client)
    await create_user_data(client, user.id, {'x': 1})
    # проверка функции Depends
    with pytest.raises(UserDataNotFound) as exc_info:
        await user_datas(user.id, CORE_ID + 'aaa', session)
    assert exc_info.value.status_code == 404


async def test_append_user_data(client):
    """
    Дозапись данных.
    При этом если есть сопадающие переменные они перетрутся новыми
    """
    user = await create_user(client)
    user_data_old = await create_user_data(client, user.id, {'x': 1, 'z': 3})
    put_data = {
        'data': {
            'x': 2,
            'y': 5,
        }
    }
    r = await client.put(
        f'/user_data/{user.id}?core_id={CORE_ID}', json=put_data
    )
    user_data_new = UserData(**r.json())
    print(user_data_new)
    assert user_data_old.data['x'] == 1
    assert user_data_new.data['x'] == 2
    assert user_data_new.data['z'] == 3
    assert user_data_new.data['y'] == 5


async def test_append_new_data(client):
    user = await create_user(client)
    put_data = {'data': {'test': 123}}
    r = await client.put(
        f'/user_data/{user.id}?core_id={CORE_ID}', json=put_data
    )
    assert r.status_code == 201
