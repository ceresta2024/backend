from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from .base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    game_money = Column(Integer)
    status = Column(Integer)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated = Column(DateTime, default=datetime.utcnow, nullable=False)
