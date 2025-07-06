from sqlalchemy import Column, Integer, String
from src.infrastructure.db.base import Base

class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)