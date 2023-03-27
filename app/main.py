from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.routes.task import router as Router

app = FastAPI()


@app.on_event('startup')
async def start_db():
    # await init_db()
    pass


@app.get('/ping', tags=['Root'])
async def pong():
    return {'ping': 'pong!'}


app.include_router(Router, prefix='/task', tags=['Task'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Instrumentator().instrument(app).expose(app)
