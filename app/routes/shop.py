# routes/shop.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Item

from app.controllers import ShopController
from app.models.base import get_session
from app.models.item import Item

# from app.schemas.shop import ItemCreate

from app.utils.auth_bearer import JWTBearer

router = APIRouter()
namespace = "shop"


@router.get("/get_store_list/")
async def get_store_list(session: Session = Depends(get_session)):
    # Implement user creation logic here
    return {"message": "Test user router"}


@router.get("/get_inventory_list/")
async def get_inventory_list(session: Session = Depends(get_session)):
    # Implement user creation logic here
    return {"message": "Test user router"}


@router.get("/sell_item/")
async def sell_item(session: Session = Depends(get_session)):
    # Implement user creation logic here
    return {"message": "Test user router"}


@router.get("/buy_item/")
async def buy_item(session: Session = Depends(get_session)):
    # Implement user creation logic here
    return {"message": "Test user router"}


@router.get("/get_items/")
async def get_items(dependencies = Depends(JWTBearer()), session: Session = Depends(get_session)):
    return ShopController(session).get_items()
