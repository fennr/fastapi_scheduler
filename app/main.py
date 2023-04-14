from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.routes.remind import router as RemindRouter
from app.routes.task import router as TaskRouter
from app.routes.user import router as UserRouter
from app.routes.user_data import router as UserDataRouter

app = FastAPI()


@app.on_event('startup')
async def start_db():
    ...
    # await init_db()


@app.get('/ping', tags=['Root'])
async def pong():
    return {'ping': 'pong!'}


app.include_router(UserRouter, prefix='/user', tags=['User'])
app.include_router(TaskRouter, prefix='/task', tags=['Task'])
app.include_router(RemindRouter, prefix='/remind', tags=['Remind'])
app.include_router(UserDataRouter, prefix='/user_data', tags=['UserData'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


Instrumentator().instrument(app).expose(app)
