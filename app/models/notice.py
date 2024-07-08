from datetime import datetime

from sqlalchemy import Column, Date, DateTime, Integer, String, Text

from .base import Base


class Notice(Base):
    __tablename__ = "notice"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contents = Column(Text, nullable=False)
    type = Column(Integer, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    is_available = Column(Integer, nullable=False)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated = Column(DateTime, default=datetime.utcnow, nullable=False)
