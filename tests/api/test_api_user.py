import pytest
from httpx import AsyncClient

from app.exceptions import UserNotFound
from app.models.user import User
from app.routes.user import get_user_by_id
from tests.data import USERS


async def create_user(
    client: AsyncClient, user_json: dict = USERS['good_user']
) -> User:
    r = await client.post('/user/', json=user_json)
    return User(**r.json())


async def test_create_user_good(client):
    r = await client.post('/user/', json=USERS['good_user'])
    assert r.status_code == 201


async def test_post_user_bad(client):
    r = await client.post('/user/', json=USERS['bad_user'])
    print(r.json())
    assert r.status_code == 422


async def test_get_user_func_good(client, session):
    user_db = await create_user(client)

    user = await get_user_by_id(user_db.id, session=session)
    assert user == user_db


async def test_get_user_func_bad(client, session):
    with pytest.raises(UserNotFound) as exc_info:
        await get_user_by_id(0, session=session)
    assert exc_info.typename == 'UserNotFound'
    assert exc_info.value.status_code == 404


async def test_get_user_api(client):
    user_db = await create_user(client)

    r = await client.get(f'/user/{user_db.id}')
    user_db = User(**r.json())
    assert user_db.id == user_db.id

    r = await client.get('/user/0')
    assert r.status_code == 404


async def test_delete_user(client):
    user = await create_user(client)
    r = await client.delete(f'/user/{user.id}')
    assert r.status_code == 200

    r = await client.delete(f'/user/{user.id}')
    assert r.status_code == 404


async def test_update_user(client):
    user_db = await create_user(client)
    user_update = USERS['good_user2']

    r = await client.put(f'/user/{user_db.id}', json=user_update)
    user2 = User(**r.json())

    assert user_db.tg == USERS['good_user']['tg']
    assert user2.tg == USERS['good_user2']['tg']
    assert user_db.tg != user2.tg
