# routes/user.py
from fastapi import APIRouter
from app.models import User

router = APIRouter()
namespace = "shop"


@router.get("/get_store_list/")
async def get_store_list():
    # Implement user creation logic here
    return {"message": "Test user router"}


@router.get("/get_inventory_list/")
async def get_inventory_list():
    # Implement user creation logic here
    return {"message": "Test user router"}


@router.get("/sell_item/")
async def sell_item():
    # Implement user creation logic here
    return {"message": "Test user router"}


@router.get("/buy_item/")
async def buy_item():
    # Implement user creation logic here
    return {"message": "Test user router"}
