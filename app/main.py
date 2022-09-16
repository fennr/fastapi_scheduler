from fastapi import FastAPI

from app.api.v1 import api_router

app = FastAPI()


@app.get("/ping", tags=["Root"])
async def pong():
    return {"ping": "pong!"}


app.include_router(api_router, prefix="/api/v1")
