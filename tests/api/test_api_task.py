import pytest

from app.exceptions import TaskException, TaskNotFound
from app.models.task import Task
from app.models.user import User
from app.routes.task import get_task_by_id
from tests.api.test_api_user import create_user
from tests.data import TASKS


async def create_task(
    client, user: User | None = None, task_json=TASKS['good_task']
):
    if not user:
        user = await create_user(client)
    task_json['user_id'] = user.id
    r = await client.post('/task/', json=task_json)
    if r.status_code not in [200, 201]:
        raise TaskException(status_code=404, detail='Test error')
    task = Task(**r.json())
    return task


async def test_create_task(client):
    task = await create_task(client)
    assert isinstance(task, Task)

    r = await client.get(f'/task/{task.id}')
    task_db = Task(**r.json())
    assert task_db.id == task.id


async def test_bad_create_task(client):
    user = await create_user(client)
    user.id = 0
    with pytest.raises(TaskException):
        await create_task(client, user, task_json=TASKS['bad_task1'])


async def test_bad_get_task_func(client, session):
    await create_user(client)
    with pytest.raises(TaskNotFound) as exc_info:
        await get_task_by_id(0, session=session)
    assert exc_info.typename == 'TaskNotFound'
    assert exc_info.value.status_code == 404


async def test_get_tasks(client):
    user = await create_user(client)
    task = await create_task(client, user)
    r = await client.get(f'/task/{task.id}?user_id={user.id}')
    task_db = Task(**r.json())
    assert task_db.user_id == user.id


async def test_update_task(client):
    user = await create_user(client)
    task_db = await create_task(client, user)
    task_update = TASKS['good_task2']

    r = await client.put(f'/task/{task_db.id}', json=task_update)
    task_2 = Task(**r.json())

    assert task_db.description != task_2.description


async def test_delete_task(client):
    task = await create_task(client)
    r = await client.delete(f'/task/{task.id}')
    task_db = Task(**r.json())
    assert task.id == task_db.id
    assert r.status_code == 200

    r = await client.delete(f'/task/{task.id}')
    assert r.status_code == 404
