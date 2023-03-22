from fastapi import FastAPI

from app.db import init_db
from app.routes.task import router as Router

app = FastAPI()


@app.on_event('startup')
async def start_db():
    await init_db()


@app.get('/ping', tags=['Root'])
async def pong():
    return {'ping': 'pong!'}


app.include_router(Router, prefix='/task', tags=['Task'])
