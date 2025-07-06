from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from src.infrastructure.db.base import Base

class QuestionModel(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    text = Column(String, nullable=False)
    scoring_rules = Column(JSON, nullable=False)

    answers = relationship("AnswerModel", backref="question", lazy="dynamic")