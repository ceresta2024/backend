# routes/user.py
from fastapi import APIRouter
from app.models import User

router = APIRouter()
namespace = "user"


@router.post("/test/")
async def test():
    # Implement user creation logic here
    return {"message": "Test user router"}
