from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Boolean, Text

from .base import Base

from app.utils import JOBS
from app.utils.const import DEFAULT_ALLOW_GOLD, DEFAULT_SPEED


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    user_name = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    game_money = Column(Integer, nullable=False, default=0)
    score = Column(Integer, nullable=False, default=0)
    job_id = Column(Integer)
    status = Column(Integer)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated = Column(DateTime, default=datetime.utcnow, nullable=False)

    @property
    def info(self):
        return {
            "id": self.id,
            "name": self.user_name,
            "email": self.email,
            "gold": self.game_money,
            "score": self.score,
            "job": JOBS["ID_TO_NAME"].get(self.job_id, ""),
            "status": self.status,
        }


class TokenTable(Base):
    __tablename__ = "token"

    user_id = Column(Integer)
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450), nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.utcnow)


class Job(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    allow_gold = Column(Integer, default=DEFAULT_ALLOW_GOLD, nullable=False)
    speed = Column(Integer, default=DEFAULT_SPEED, nullable=False)
    enabled = Column(Boolean, default=True)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated = Column(DateTime, default=datetime.utcnow, nullable=False)


class Skill(Base):
    __tablename__ = "skill"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    attributes = Column(Text, nullable=False)
    job_id = Column(Integer)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated = Column(DateTime, default=datetime.utcnow, nullable=False)
