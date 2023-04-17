import pytest

from app.exceptions import RemindNotFound
from app.models.remind import Remind
from app.models.task import Task
from app.routes.remind import get_remind_by_id
from tests.api.test_api_task import create_task
from tests.data import REMINDS


async def create_remind(
    client, task: Task | None = None, remind_json=REMINDS['good_remind']
):
    if not task:
        task = await create_task(client)
    remind_json['task_id'] = task.id
    r = await client.post('/remind/', json=remind_json)
    if r.status_code not in [200, 201]:
        raise RemindNotFound(status_code=404, detail='Test error')
    remind = Remind(**r.json())
    return remind


async def test_create_remind(client):
    remind = await create_remind(client)
    assert isinstance(remind, Remind)


async def test_get_remind_func(client, session):
    remind_db = await create_remind(client)
    remind1 = await get_remind_by_id(remind_id=remind_db.id, session=session)
    assert remind1 == remind_db

    r = await client.get(f'/remind/{remind_db.id}')
    remind = Remind(**r.json())
    assert remind_db == remind


async def test_get_remind_func_bad(client, session):
    remind_db = await create_remind(client)
    with pytest.raises(RemindNotFound):
        await get_remind_by_id(remind_id=remind_db.id + 1, session=session)

    r = await client.get(f'/remind/{remind_db.id + 1}')
    assert r.json()['detail'].endswith('not found')


async def test_update_remind(client):
    new_dtime = '2023-04-17T07:09:20'
    remind = await create_remind(client)
    data = {'dtime': new_dtime}
    r = await client.put(f'/remind/{remind.id}', json=data)
    new_remind = Remind(**r.json())
    assert remind.dtime != new_remind.dtime


async def test_delete_remind(client):
    remind = await create_remind(client)
    r = await client.delete(f'/remind/{remind.id}')
    remind_db = Remind(**r.json())
    assert remind.id == remind_db.id
    assert r.status_code == 200

    r = await client.delete(f'/remind/{remind.id}')
    assert r.status_code == 404
