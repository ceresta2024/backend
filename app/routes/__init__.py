# app/routes/__init__.py

from fastapi import APIRouter
from app.routes import user

# Create an API router
router = APIRouter()

# Include your route modules
router.include_router(user.router, prefix="/users", tags=["users"])
# Add more route modules as needed

# You can also define additional common routes here if necessary
# For example:
# router.include_router(some_other_module.router, prefix="/other", tags=["other"])

# Export the router for use in your main FastAPI app
__all__ = ["router"]
