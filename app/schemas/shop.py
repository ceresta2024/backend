from pydantic import BaseModel, Field


class StoreList(BaseModel):
    id: int
    item_id: int
    name: str
    price: int
    quantity: int


class InventoryList(BaseModel):
    name: int
    item_id: int
    quantity: int
    price: int
    function: int
    hp: str
    sp: str
    duration: str


class RequestBuyItem(BaseModel):
    item_id: int
    quantity: int


class RequestSellItem(BaseModel):
    item_id: int
    quantity: int
