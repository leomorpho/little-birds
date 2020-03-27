from fastapi import FastAPI
from pydantic import BaseModel
from app.infrastructure.router import router    

api = FastAPI()

@api.get("/")
async def hello():
    return {"message": "Hello there!"}

api.include_router(router)