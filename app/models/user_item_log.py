from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey, orm

from .base import Base


class UserItemLog(Base):
    __tablename__ = "user_item_log"

    id = Column(Integer, primary_key=True, index=True)
    picked_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    # User relationship
    user_id: str = Column(Integer, ForeignKey("user.id"))
    user = orm.relationship("Package")

    # Item relationship
    item_id: str = Column(Integer, ForeignKey("item.id"))
    item = orm.relationship("Package")

    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated = Column(DateTime, default=datetime.utcnow, nullable=False)
