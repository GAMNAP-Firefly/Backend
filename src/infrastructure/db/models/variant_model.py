from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.infrastructure.db.base import Base

class VariantModel(Base):
    __tablename__ = "variants"

    id = Column(Integer, primary_key=True)
    var_text = Column(String, nullable=False)

    answers = relationship("AnswerModel", backref="variant")