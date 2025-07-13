from pydantic import BaseModel
from typing import List

class HRResultsByLinkResponse(BaseModel):
    candidate_analysis: dict  # CandidateAnalysisDTO
    category_scores: List[dict]  # List[CategoryScoreDTO] 