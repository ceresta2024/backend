from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Boolean

from .base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    user_name = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    game_money = Column(Integer)
    status = Column(Integer)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated = Column(DateTime, default=datetime.utcnow, nullable=False)


class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_toke = Column(String(450), primary_key=True)
    refresh_toke = Column(String(450), nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.utcnow)
