from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.item import Item
from app.models.shop import Shop

# from app.schemas.shop import ItemCreate


class ShopController:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_items(self) -> list[Item]:
        return self.session.query(Item).all()

    def get_store_list(self) -> list[Shop]:
        return self.session.query(Shop).all()
