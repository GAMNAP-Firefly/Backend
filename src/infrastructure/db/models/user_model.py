from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from src.infrastructure.db.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    results = relationship("ResultModel", backref="user", cascade="all, delete-orphan")
    answers = relationship("AnswerModel", backref="user", lazy="dynamic")
