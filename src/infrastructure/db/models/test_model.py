from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.infrastructure.db.base import Base

class TestModel(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    questions = relationship("QuestionModel", backref="test", cascade="all", lazy="dynamic")
    results = relationship("ResultModel", backref="test")