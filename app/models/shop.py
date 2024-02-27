from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey, orm

from .base import Base
from .item import Item


class Shop(Base):
    __tablename__ = "shop"

    id = Column(Integer, primary_key=True, index=True)
    
    item_id: int = Column(Integer, ForeignKey("item.id"))
    item = orm.relationship("Item")

    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated = Column(DateTime, default=datetime.utcnow, nullable=False)
