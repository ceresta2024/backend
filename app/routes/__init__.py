# app/routes/__init__.py

from fastapi import APIRouter
from app.routes import game, user, shop

# Create an API router
router = APIRouter()

# Include your route modules
router.include_router(user.router, prefix="/user", tags=["user"])
router.include_router(game.router, prefix="/game", tags=["game"])
router.include_router(shop.router, prefix="/shop", tags=["shop"])

# Export the router for use in your main FastAPI app
__all__ = ["router"]
