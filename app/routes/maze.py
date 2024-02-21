# routes/user.py
from fastapi import APIRouter
from app.models import User

router = APIRouter()
namespace = "maze"


@router.get("/get_starttime/")
async def get_starttime():
    # Implement user creation logic here
    return {"message": "Test user router"}


@router.get("/is_open/")
async def is_open():
    # Implement user creation logic here
    return {"message": "Test user router"}

