# app/routes/__init__.py

from fastapi import APIRouter
from app.routes import user, maze, shop

# Create an API router
router = APIRouter()

# Include your route modules
router.include_router(user.router, prefix="/user", tags=["user"])
router.include_router(maze.router, prefix="/maze", tags=["maze"])
router.include_router(shop.router, prefix="/shop", tags=["shop"])

# Export the router for use in your main FastAPI app
__all__ = ["router"]
