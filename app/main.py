# main.py

from fastapi import FastAPI
from app.config import settings
from app.routes import user
from celery import Celery


app = FastAPI()

celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

# Include your API routers
app.include_router(user.router, prefix="/users", tags=["users"])


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI project!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
