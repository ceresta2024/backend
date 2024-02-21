# main.py

from fastapi import FastAPI
from app.config import settings
from app.routes import user, maze, shop


app = FastAPI()

# Include specific API routers
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(maze.router, prefix="/maze", tags=["maze"])
app.include_router(shop.router, prefix="/shop", tags=["shop"])


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI project!"}
