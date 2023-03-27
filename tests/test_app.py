from fastapi.testclient import TestClient


async def test_app(client: TestClient):
    r = await client.get('/ping')
    data = r.json()
    assert data['ping'] == 'pong!'
