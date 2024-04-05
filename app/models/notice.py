from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Text

from .base import Base


class Notice(Base):
    __tablename__ = "notice"

    id = Column(Integer, primary_key=True, index=True)
    contents = Column(Text, nullable=False)
    type = Column(Integer, nullable=False)
    is_available = Column(Integer, nullable=False)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated = Column(DateTime, default=datetime.utcnow, nullable=False)
