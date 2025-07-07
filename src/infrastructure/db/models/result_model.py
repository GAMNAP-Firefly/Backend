from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Text
from sqlalchemy.orm import relationship
from src.infrastructure.db.base import Base
from datetime import datetime

class ResultModel(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    status = Column(String, nullable=False)
    link_token = Column(String(32), unique=True, nullable=True)
    interpretation = Column(Text, nullable=True)

    answers = relationship("AnswerModel", backref="result", cascade="all, delete-orphan", lazy="dynamic")