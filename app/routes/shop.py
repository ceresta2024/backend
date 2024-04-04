# routes/shop.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Item

from app.controllers import ShopController
from app.models.base import get_session
from app.models.item import Item
from app.schemas.shop import RequestBuyItem
from app.utils.auth_bearer import JWTBearer, decodeJWT

router = APIRouter()
namespace = "shop"


@router.get("/get_store_list/")
async def get_store_list(session: Session = Depends(get_session)):
    return ShopController(session).get_store_list()


@router.get("/get_inventory_list/")
async def get_inventory_list(token=Depends(JWTBearer()), session: Session = Depends(get_session)):
    user_id = decodeJWT(token)["sub"]
    return ShopController(session).get_inventory_list(user_id)


@router.post("/sell_item/")
async def sell_item(
    request: RequestBuyItem,
    token=Depends(JWTBearer()),
    session: Session = Depends(get_session),
):
    return ShopController(session).sell_item()


@router.post("/buy_item/")
async def buy_item(
    request: RequestBuyItem,
    token=Depends(JWTBearer()),
    session: Session = Depends(get_session),
):
    user_id = decodeJWT(token)["sub"]
    return ShopController(session).buy_item(request, user_id)


@router.get("/get_items/")
async def get_items(
    token=Depends(JWTBearer()), session: Session = Depends(get_session)
):
    return ShopController(session).get_items()
