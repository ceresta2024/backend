from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.inventory import Inventory
from app.models.item import Item
from app.models.shop import Shop
from app.schemas.shop import StoreList, RequestBuyItem
from app.utils.common import get_list_of_dict


class ShopController:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_items(self) -> list[Item]:
        return self.session.query(Item).all()

    def get_store_list(self) -> list:
        data = (
            self.session.query(Shop.id, Item.id, Item.name, Shop.price, Shop.quantity)
            .join(Shop, Shop.item_id == Item.id)
            .filter(Shop.quantity > 0)
            .all()
        )
        return get_list_of_dict(StoreList.__fields__.keys(), data)

    def buy_item(self, request: RequestBuyItem, user_id: int):
        shop_item = (
            self.session.query(Shop).filter(Shop.item_id == request.item_id).first()
        )
        if shop_item is None or shop_item.quantity == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item doesn't exist on shop",
            )
        if request.quantity <= 0 or request.quantity > shop_item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item quantity is insufficient",
            )

        shop_item.quantity -= request.quantity
        inven = (
            self.session.query(Inventory)
            .filter_by(user_id=user_id, item_id=request.item_id)
            .first()
        )
        if inven:
            inven.quantity += request.quantity
        else:
            inven = Inventory(
                user_id=user_id, item_id=request.item_id, quantity=request.quantity
            )
            self.session.add(inven)
        self.session.commit()
        return {"message": "finished successfully"}

    def sell_item(self):
        return {}
