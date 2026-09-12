from fastapi import FastAPI
from app.router.system import router

app = FastAPI()

app.include_router(router)