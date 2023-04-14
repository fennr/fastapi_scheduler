import pytest
from fastapi import HTTPException

from app.models.task import Task
from tests.data import TASKS, USERS


async def create_user(client, user_json=USERS['good_user']):
    await client.post('/user/', json=user_json)


async def create_task(client, task_json=TASKS['good_task']):
    r = await client.post('/task/', json=task_json)
    if r.status_code not in [200, 201]:
        raise HTTPException(status_code=404)
    task = Task(**r.json())
    return task


async def test_create_task(client):
    await create_user(client)
    task = await create_task(client)
    assert isinstance(task, Task)

    r = await client.get(f'/task/{task.id}')
    task_db = Task(**r.json())
    assert task_db.id == task.id


async def test_bad_get_task1(client):
    await create_user(client)
    with pytest.raises(HTTPException):
        await create_task(client, task_json=TASKS['bad_task1'])


async def test_bad_get_task2(client):
    await create_user(client)
    with pytest.raises(HTTPException):
        await create_task(client, task_json=TASKS['bad_task2'])


async def test_update_task(client):
    await create_user(client)
    task_db = await create_task(client)
    task_update = TASKS['good_task2']

    r = await client.put(f'/task/{task_db.id}', json=task_update)
    task_2 = Task(**r.json())

    assert task_db.description != task_2.description
