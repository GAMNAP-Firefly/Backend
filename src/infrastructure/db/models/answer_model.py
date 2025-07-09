from sqlalchemy import Column, Integer, ForeignKey

from src.infrastructure.db.base import Base


class AnswerModel(Base):
    __tablename__ = "answers"

    question_id = Column(Integer, ForeignKey("questions.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    variant_id = Column(Integer, ForeignKey("variants.id"), primary_key=True)
    result_id = Column(Integer, ForeignKey("results.id"), primary_key=True)
