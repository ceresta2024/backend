from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.item import Item
from app.models.shop import Shop
from app.schemas.shop import StoreList
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
