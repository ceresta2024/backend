from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created = Column(DateTime, default=datetime.utcnow)
