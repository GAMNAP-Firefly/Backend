from pydantic import BaseModel

class CandidateAnalysisResponse(BaseModel):
    test_name: str
    start_time: str
    end_time: str
    duration_minutes: float
    interpretation: str 