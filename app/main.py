# main.py

from fastapi import FastAPI
from app.config import settings
from app.routes import router
from app.sockets import sio_app


app = FastAPI()

# Include router
app.include_router(router)

app.mount("/", sio_app)
