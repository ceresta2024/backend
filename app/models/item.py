from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from .base import Base


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    hp = Column(Integer, nullable=True)
    sp = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)
    group = Column(Text, nullable=False)
    function = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    img_path = Column(Text, nullable=False)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated = Column(DateTime, default=datetime.utcnow, nullable=False)
