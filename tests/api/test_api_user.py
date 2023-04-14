from httpx import AsyncClient

from app.models.user import User
from tests.data import USERS


async def create_user(
    client: AsyncClient, user_json: dict = USERS['good_user']
) -> User:
    r = await client.post('/user/', json=user_json)
    return User(**r.json())


async def test_create_user(client):
    r = await client.post('/user/', json=USERS['good_user'])
    assert r.status_code == 201


async def test_bad_user(client):
    r = await client.post('/user/', json=USERS['bad_user'])
    assert r.status_code == 422


async def test_get_user(client):
    user_db = await create_user(client)
    r = await client.get(f'/user/{user_db.id}')
    user = User(**r.json())
    assert user.id == user_db.id


async def test_delete_user(client):
    user = await create_user(client)
    r = await client.delete(f'/user/{user.id}')
    print(r.json())
    assert r.status_code == 200


async def test_update_user(client):
    user_db = await create_user(client)
    user_update = USERS['good_user2']

    r = await client.put(f'/user/{user_db.id}', json=user_update)
    user2 = User(**r.json())

    assert user_db.tg == USERS['good_user']['tg']
    assert user2.tg == USERS['good_user2']['tg']
    assert user_db.tg != user2.tg
