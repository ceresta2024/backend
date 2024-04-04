from pydantic import BaseModel


class StoreList(BaseModel):
    id: int
    item_id: int
    name: str
    price: int
    quantity: int
