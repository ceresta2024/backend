from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.item import Item
from app.models.shop import Shop
from app.models.user import User
from app.schemas.shop import StoreList, InventoryList, RequestBuyItem, RequestSellItem
from app.utils.common import get_list_of_dict

BUY_SELL_RATIO = 0.9


class ShopController:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_store_list(self, keyword: str) -> dict:
        filter_args = []
        filter_args.append(Shop.quantity > 0)
        if keyword:
            filter_args.append(Item.name.ilike(f"%{keyword}%"))
        data = (
            self.session.query(Shop.id, Item.id, Item.name, Shop.price, Shop.quantity)
            .join(Shop, Shop.item_id == Item.id)
            .filter(*filter_args)
            .all()
        )
        items = get_list_of_dict(StoreList.__fields__.keys(), data)
        return {"data": items}

    def get_inventory_list(self, user_id: int, keyword: str) -> dict:
        filter_args = [Inventory.user_id == user_id, Inventory.quantity > 0]
        if keyword:
            filter_args.append(Item.name.ilike(f"%{keyword}%"))
        data = (
            self.session.query(
                Item.name, Inventory.item_id, Inventory.quantity, Shop.price, Item.function, Item.hp, Item.sp, Item.duration
            )
            .join(Inventory, Inventory.item_id == Item.id)
            .join(Shop, Shop.item_id == Item.id)
            .filter(*filter_args)
            .all()
        )
        items = get_list_of_dict(InventoryList.__fields__.keys(), data)
        for item in items:
            item["price"] = int(item["price"] * BUY_SELL_RATIO)
        return {"data": items}

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
        user = self.session.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect token"
            )
        price = int(request.quantity * shop_item.price)
        if user.game_money < price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="gold is insufficient"
            )
        user.game_money -= price
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

    def sell_item(self, request: RequestSellItem, user_id: int):
        inven = (
            self.session.query(Inventory)
            .filter_by(user_id=user_id, item_id=request.item_id)
            .first()
        )
        if inven is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item doesn't exist on inventory",
            )
        if inven.quantity < request.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The sales quantity is not correct",
            )

        shop_item = (
            self.session.query(Shop).filter(Shop.item_id == request.item_id).first()
        )
        if shop_item is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This item is no longer for sale.",
            )

        user = self.session.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect token"
            )
        price = int(BUY_SELL_RATIO * shop_item.price * request.quantity)
        user.game_money += price
        inven.quantity -= request.quantity
        self.session.commit()
        return {"message": "finished successfully"}
