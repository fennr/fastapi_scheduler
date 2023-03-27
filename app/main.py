from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.db import init_db
from app.routes.schedule import router as ScheduleRouter
from app.routes.task import router as TaskRouter

app = FastAPI()


@app.on_event('startup')
async def start_db():
    await init_db()


@app.get('/ping', tags=['Root'])
async def pong():
    return {'ping': 'pong!'}


app.include_router(TaskRouter, prefix='/task', tags=['Task'])
app.include_router(ScheduleRouter, prefix='/schedule', tags=['Schedule'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Instrumentator().instrument(app).expose(app)
