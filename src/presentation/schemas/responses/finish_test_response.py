from pydantic import BaseModel
from typing import List, Optional

class CategoryScoreResponse(BaseModel):
    category_name: str
    score: float

class HRShareLinkResponse(BaseModel):
    share_code: str

class FinishTestResponse(BaseModel):
    results: List[CategoryScoreResponse]
    share_link: Optional[HRShareLinkResponse] = None 