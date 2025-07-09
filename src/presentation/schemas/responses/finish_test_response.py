from pydantic import BaseModel
from typing import List

class CategoryScoreResponse(BaseModel):
    category_name: str
    score: float

class FinishTestResponse(BaseModel):
    results: List[CategoryScoreResponse] 