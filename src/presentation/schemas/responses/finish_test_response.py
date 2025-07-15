from pydantic import BaseModel
from typing import List, Optional


class CategoryScoreResponse(BaseModel):
    category_name: str
    score: float


class HRShareLinkResponse(BaseModel):
    share_code: str


class CandidateAnalysisResponse(BaseModel):
    test_name: str
    start_time: str
    end_time: str
    duration_minutes: float
    interpretation: str


class FinishTestResponse(BaseModel):
    candidate_analysis: Optional[CandidateAnalysisResponse]
    results: List[CategoryScoreResponse]
    share_link: Optional[HRShareLinkResponse] = None
