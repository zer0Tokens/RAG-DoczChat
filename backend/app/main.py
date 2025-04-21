from fastapi import FastAPI
from app.api import routers

app = FastAPI()

app.include_router(routers.upload.router)
app.include_router(routers.chat.router)
