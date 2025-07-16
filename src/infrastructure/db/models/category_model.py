from sqlalchemy import Column, Integer, String, Float

from src.infrastructure.db.base import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    mean = Column(Float, nullable=True)
    deviation = Column(Float, nullable=True)
