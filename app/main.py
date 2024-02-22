# main.py

from fastapi import FastAPI
from app.config import settings
from app.routes import router


app = FastAPI()

# Include router
app.include_router(router)
