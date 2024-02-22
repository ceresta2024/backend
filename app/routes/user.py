# routes/user.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import UserController
from app.models.base import obtain_session

router = APIRouter()
namespace = "user"


@router.post("/login/")
async def login():
    # Implement user creation logic here
    return {"message": "Test user router"}


@router.post("/register/")
async def register():
    # Implement user creation logic here
    return {"message": "Test user router"}


@router.post("/change_account/")
async def change_account():
    # Implement user creation logic here
    return {"message": "Test user router"}


@router.post("/change_password/")
async def change_password():
    # Implement user creation logic here
    return {"message": "Test user router"}


@router.get("/get_nickname/")
async def get_nickname(session: Session = Depends(obtain_session)):
    return UserController(session).get_nickname()
