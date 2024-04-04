from pydantic import BaseModel, Field


class StoreList(BaseModel):
    id: int
    item_id: int
    name: str
    price: int
    quantity: int


class RequestBuyItem(BaseModel):
    item_id: int
    quantity: int
