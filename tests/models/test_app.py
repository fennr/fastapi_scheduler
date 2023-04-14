import pytest

from app import __version__


def test_version():
    assert __version__ == '0.1.0'


@pytest.mark.asyncio
async def test_app(client):
    r = await client.get('/ping')
    data = r.json()
    assert data['ping'] == 'pong!'
