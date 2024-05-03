from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey, orm

from .base import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)

    user_id: int = Column(Integer, ForeignKey("user.id"))
    user = orm.relationship("User")

    item_id: int = Column(Integer, ForeignKey("item.id"))
    item = orm.relationship("Item")

    quantity = Column(Integer, nullable=False)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated = Column(DateTime, default=datetime.utcnow, nullable=False)
